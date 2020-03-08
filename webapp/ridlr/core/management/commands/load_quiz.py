import json
from django.core.management.base import BaseCommand, CommandError
from core.models import (Category, SubCategory, Quiz, QuizStructure, \
    Question, Choice)

class Command(BaseCommand):
    help = 'Load Quiz from TSV'

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
                print("Parsed:")
                print(json.dumps(results, indent=1))
