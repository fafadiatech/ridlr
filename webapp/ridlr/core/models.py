from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category)

    def __str__(self):
        return self.name

class Quiz(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category)
    sub_category = models.ForeignKey(SubCategory)
    timed = models.BooleanField(default=False)
    time_limit = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.category}-{self.id}-{self.name}"

class QuizStructure(models.Model):
    quiz = models.ForeignKey()
    category = models.ForeignKey(Category)
    sub_category = models.ForeignKey(SubCategory)
    frequency = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.category}-{self.id}-{self.name}"

class Question(models.Model):
    blurb = models.TextField()
    category = models.ForeignKey(Category)
    sub_category = models.ForeignKey(SubCategory)

class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice = models.CharField(max_length=255)
    correct = models.BooleanField(default=False)

class Invitation(models.Model):
    pass

class TestSession(models.Model):
    pass

class QuestionResponse(models.Model):
    pass
