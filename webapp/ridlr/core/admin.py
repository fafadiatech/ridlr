from django.contrib import admin
from .models import (Category, SubCategory, Quiz, \
    QuizStructure, QuestionType, Question, Choice, Invitation, \
    TestSession, QuestionResponse, QuestionBank)

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Quiz)
admin.site.register(QuizStructure)
admin.site.register(QuestionType)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Invitation)
admin.site.register(QuestionBank)
admin.site.register(TestSession)
admin.site.register(QuestionResponse)