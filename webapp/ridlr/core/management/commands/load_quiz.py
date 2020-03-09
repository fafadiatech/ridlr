import json
from django.core.management.base import BaseCommand, CommandError
from core.models import (Category, SubCategory, Quiz, QuizStructure, \
    Question, Choice, QuestionType)

class Command(BaseCommand):
    help = 'Load Quiz from TSV'
    DEBUG = False

    def add_arguments(self, parser):
        parser.add_argument('tsv_file', nargs='+', type=str)

    def handle(self, *args, **options):
        for current in options['tsv_file']:
            with open(current) as input_file:
                results = {}
                parser_state = ""
                current_question_id = 0
                for row in input_file.readlines():
                    row = row.strip()
                    tokens = row.split("\t")
                    if tokens[0] == "##" or tokens[0] == "":
                        continue
                    elif parser_state == "" and tokens[0] == "Quiz":
                        results["quiz"] = tokens[1]
                        parser_state = "parsed_quiz"
                    elif parser_state == "parsed_quiz" and tokens[0] == "Timed":
                        results["timed"] = tokens[1]
                        parser_state = "parsed_timed"
                    elif parser_state == "parsed_timed" and tokens[0] == "Max Time In Mins":
                        results["max_time_in_mins"] = tokens[1]
                        parser_state = "parsed_max_time"
                    elif parser_state == "parsed_max_time" and tokens[0] == "Quiz Structure":
                        parser_state = "parse_quiz_structure"
                    elif parser_state == "parse_quiz_structure":
                        if "quiz_structure" not in results:
                            results["quiz_structure"] = []
                        # change state to parsing question bank
                        if tokens[0] == "Category":
                            parser_state = "parse_qb"
                            continue

                        # update quiz structure
                        current_qs = {}
                        k, v = tokens
                        current_qs[k] = int(v)
                        results["quiz_structure"].append(current_qs)
                    elif parser_state == "parse_qb":
                        # it is a question line
                        if len(tokens) > 2:
                            category, sub_category, question_type, point, question, choice = tokens[:6]

                            correct = ""
                            if len(tokens) > 6 and tokens[6] != "":
                                correct = tokens[6]

                            if "questions" not in results:
                                results["questions"] = {}
                            results["questions"][current_question_id] = {}
                            results["questions"][current_question_id]["category"] = category
                            results["questions"][current_question_id]["sub_category"] = sub_category
                            results["questions"][current_question_id]["question_type"] = question_type
                            results["questions"][current_question_id]["point"] = point
                            results["questions"][current_question_id]["question"] = question
                            results["questions"][current_question_id]["choices"] = []
                            current_choice = {}
                            current_choice["caption"] = choice
                            if correct == "Y":
                                current_choice["correct"] = True
                            else:
                                current_choice["correct"] = False
                            results["questions"][current_question_id]["choices"].append(current_choice)
                            current_question_id += 1
                        else:
                            # append to choices
                            current_choice = {}
                            current_choice["caption"] = tokens[0]
                            if len(tokens) > 1 and tokens[1] == "Y":
                                current_choice["correct"] = True
                            else:
                                current_choice["correct"] = False
                            results["questions"][current_question_id-1]["choices"].append(current_choice)
                    else:
                        print(f"At {parser_state}: Cannot parse {row}")

                if self.DEBUG:
                    print("Parsed:")
                    print(json.dumps(results, indent=1))

                uniq_categories = []

                for current in results['questions']:
                    current_category = results['questions'][current]['category']
                    if current_category not in uniq_categories:
                        uniq_categories.append(current_category)

                # create categories
                for current in uniq_categories:
                    if not Category.objects.filter(name=current).exists():
                        category = Category()
                        category.name = current
                        category.save()

                # create sub-categories
                for current in results['questions']:
                    current_category = results['questions'][current]["category"]
                    category = Category.objects.get(name=current_category)
                    current_sub_category = results['questions'][current]["sub_category"]
                    if not SubCategory.objects.filter(name=current_sub_category).exists():
                        sub_category = SubCategory()
                        sub_category.category = category
                        sub_category.name = current_sub_category
                        sub_category.save()

                # create quiz
                quiz = None
                if Quiz.objects.filter(name=results["quiz"]).exists():
                    raise CommandError(f"Quiz {results['quiz']} already exists")
                else:
                    quiz = Quiz()
                    quiz.name = results['quiz']
                    quiz.category = Category.objects.get(name=uniq_categories[0])
                    quiz.sub_category = SubCategory.objects.filter(category=quiz.category).first()
                    if results['timed'] == "Y":
                        quiz.timed = True
                    else:
                        quiz.timed = False
                    quiz.time_limit = int(results['max_time_in_mins'])
                    quiz.save()

                # create quiz structure
                for current in results['quiz_structure']:
                    quiz_structure = QuizStructure()
                    quiz_structure.quiz = quiz
                    quiz_structure.category = Category.objects.get(name=uniq_categories[0])
                    sub_category, frequency = list(current.keys())[0], list(current.values())[0]
                    quiz_structure.sub_category = SubCategory.objects.get(name=sub_category, category=quiz_structure.category)
                    quiz_structure.frequency = frequency
                    quiz_structure.save()

                # create question type
                for current in results['questions']:
                    current_question_type = results['questions'][current]["question_type"]
                    if not QuestionType.objects.filter(name=current_question_type).exists():
                        question_type = QuestionType()
                        question_type.name = current_question_type
                        question_type.save()

                # create question & choices
                for current in results['questions']:
                    question = Question()
                    question.category = Category.objects.get(name=results['questions'][current]["category"])
                    question.sub_category = SubCategory.objects.get(name=results['questions'][current]["sub_category"], category=category)
                    question.question_type = QuestionType.objects.get(name=results['questions'][current]["question_type"])
                    question.point = results['questions'][current]["point"]
                    question.blurb = results['questions'][current]["question"]
                    question.save()

                    for current_choice in results['questions'][current]["choices"]:
                        choice = Choice()
                        choice.question = question
                        choice.choice = current_choice['caption']
                        choice.correct = current_choice['correct']
                        choice.save()