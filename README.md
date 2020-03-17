# Ridlr

Ridlr is simple Online Tutoring & Quiz application written in Django

## Setting up

Ridlr setup is relatively simpler. It used `Django` for API layer, specifically we're using [Django REST Framework](https://www.django-rest-framework.org/). Frontend is written using `ReactJS`.

### Backend

1. Create virtualenv `python3.7 -m venv venv`
1. Activate virtualenv `source ./venv/bin/activate`
1. Create Database `cd webapp/ridlr && python manage.py migrate`
    1. NOTE: Change `settings.py` if you would like to run Ridlr with different Database
1. Create Superuser `python manage.py createsuperuser`
1. Load Quiz using following management command `python manage.py load_quiz ./master_templates/Quiz-Template.tsv`
    1. Replace with any Quiz Template that you might have created
1. Start Django `python manage.py runserver 0.0.0.0:8000`


### Frontend

1. Change to right directory `cd webapp/ridlr/frontend/ridlr`
2. Install Dependencies `yarn install`
3. Start the frontend `yarn serve`


## Models

1. `Category`:
1. `SubCategory`: 
1. `Quiz`:
1. `QuizStructure`:
1. `QuestionType`:
1. `Question`: 
1. `Choice`: 
1. `QuestionBank`:
1. `Invitation`:
1. `TestSession`:
1. `QuestionResponse`: 
