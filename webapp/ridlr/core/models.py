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

class QuizStructure(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    frequency = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.category}-{self.id}-{self.name}"

class Question(models.Model):
    blurb = models.TextField()
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

class Invitation(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    invitation_for = models.ForeignKey(User, on_delete=models.CASCADE)
    invitation_code = models.CharField(max_length=25)
    ts = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.quiz}-{self.invitation_for}-{self.invitation_code}"

class TestSession(models.Model):
    invitation = models.ForeignKey(Invitation, on_delete=models.CASCADE)
    started_ts = models.DateTimeField(default=timezone.now)
    completed_ts = models.DateTimeField(blank=True, null=True, default=None)

    def __str__(self):
        return f"{self.invitation}-{self.started_ts}-{self.completed_ts}"

class QuestionResponse(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    response = models.TextField()
    ts = models.DateTimeField(default=timezone.now)
    
