from django.contrib import admin
from .models import (Category, SubCategory, Quiz, \
    QuizStructure, Question, Choice, Invitation, \
    TestSession, QuestionResponse)

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Quiz)
admin.site.register(QuizStructure)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Invitation)
admin.site.register(TestSession)
admin.site.register(QuestionResponse)