import random
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Sub Categories"

    def __str__(self):
        return self.name

class Quiz(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    timed = models.BooleanField(default=False)
    time_limit = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Quizes"

    def __str__(self):
        return f"{self.category}-{self.id}-{self.name}"

# this tell Ridlr, how to generate QuestionBank
# basically tuple of sub_category, frequency mapping
class QuizStructure(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    frequency = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.id}-{self.quiz}-{self.category}-{self.sub_category}"

class QuestionType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Question(models.Model):
    blurb = models.TextField()
    question_type = models.ForeignKey(QuestionType, on_delete=models.CASCADE)
    point = models.IntegerField(default=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.category}-{self.id}-{self.blurb}"

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.CharField(max_length=255)
    correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.question}-{self.choice}"

# this is the model that stores sequence
# of question that needs to filled in
class QuestionBank(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    questions = models.ManyToManyField(Question)

    @classmethod
    def generate(self, invitation_code):
        invitation = Invitation.objects.get(invitation_code=invitation_code)
        quiz = invitation.quiz
        results = {}
        results['quiz'] = quiz.name
        results['timed'] = quiz.timed
        results['time_limit'] = quiz.time_limit
        question_bank = random.choice(QuestionBank.objects.filter(quiz=quiz))
        results['questions'] = []
        for current in question_bank.questions.all():
            row = {}
            row["id"] = current.id
            row["question"] = current.blurb
            row["question_type"] = current.question_type.name
            row["point"] = current.point
            row["sub_category"] = current.sub_category.name
            row["choices"] = []

            correct_choice_id = 0
            for current_choice in Choice.objects.filter(question=current):
                choice_row = {}
                choice_row["id"] = current_choice.id
                choice_row["choice"] = current_choice.choice
                choice_row["correct"] = current_choice.correct

                if current_choice.correct:
                    correct_choice_id = current_choice.id

                row["choices"].append(choice_row)
            random.shuffle(row["choices"])
            row['correct_choice_id'] = correct_choice_id
            results["questions"].append(row)
        # invitation.consumed = True
        # invitation.save()
        random.shuffle(results["questions"])

        return results

    def __str__(self):
        return f"{self.quiz}-{self.id}"

class Invitation(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    invitation_for = models.ForeignKey(User, on_delete=models.CASCADE)
    invitation_code = models.CharField(max_length=25)
    consumed = models.BooleanField(default=False)
    ts = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.quiz}-{self.invitation_for}-{self.invitation_code}"

class TestSession(models.Model):
    invitation = models.ForeignKey(Invitation, on_delete=models.CASCADE)
    question_bank = models.ForeignKey(QuestionBank, on_delete=models.CASCADE)
    started_ts = models.DateTimeField(default=timezone.now)
    completed_ts = models.DateTimeField(blank=True, null=True, default=None)

    def __str__(self):
        return f"{self.invitation}-{self.started_ts}-{self.completed_ts}"

class QuestionResponse(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    response = models.TextField()
    ts = models.DateTimeField(default=timezone.now)
    
