import random
from collections import defaultdict
from django.core.management.base import BaseCommand, CommandError
from core.models import (Quiz, QuizStructure, Question, QuestionBank)

class Command(BaseCommand):
    help = 'Generates Question Bank given Quiz ID'
    DEBUG = False

    def add_arguments(self, parser):
        parser.add_argument('quiz_id', nargs='+', type=str)

    def handle(self, *args, **options):
        for quiz_id in options['quiz_id']: 
            quiz_id = int(quiz_id)

            if not Quiz.objects.filter(id=quiz_id).exists():
                raise CommandError(f"Quiz with ID {quiz_id} doesn't exists")

            quiz = Quiz.objects.get(id=quiz_id)
            
            processed = defaultdict(int)
            chosen_questions = []

            for current in QuizStructure.objects.filter(quiz=quiz):
                questions = [current_question.id for current_question in Question.objects.filter(category=current.category, sub_category=current.sub_category)]
                key = "%s\t%s" % (current.category, current.sub_category)

                while processed[key] < current.frequency:
                    candidate = random.choice(questions)
                    if candidate in chosen_questions:
                        continue
                    chosen_questions.append(candidate)
                    processed[key] += 1

            question_bank = QuestionBank()
            question_bank.quiz = quiz
            question_bank.save()
            question_bank.questions.set(chosen_questions)
            question_bank.save()
            print("Completed Genrating Questions")

