from django.core.management.base import BaseCommand, CommandError
from core.models import (Category, SubCategory, Quiz, QuizStructure, \
    Question, Choice)

class Command(BaseCommand):
    help = 'Load Quiz from TSV'

    def add_arguments(self, parser):
        parser.add_argument('tsv_file', nargs='+', type=str)

    def handle(self, *args, **options):
        for current in options['tsv_file']:
            print(current)