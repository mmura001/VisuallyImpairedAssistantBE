## The main perspective of the project to help assist the visually impaired to speak perform actions to fullfill the user requirements by generating the actions and also trigger the actions.

## Below are the steps to perform in order to setup a django project

### Install python if not available

`https://www.python.org/downloads/macos/`

### create Virtual environment 

`python3 -m venv ./devenv`

### Activate Virtual Environment

`source devenv/bin/activate`

### Install the existing requirements to run this project
`pip install -r requirements.txt`

### to freeze the append the newly added libraries to requirements.txt
`pip freeze > requirements.txt`


### Install all the Django libraries required if you want to setup a new project

 pip install django

### To start a new project in django

 `python -m django startproject backend`

### navigate to backend folder and  to create the app
`python manage.py startapp myApi`

### Allow all calls from other apps in settings.py
`CORS_ALLOW_ALL_ORIGINS = True`

### Make migrations when you change anything in models
`python manage.py makemigrations`
`python manage.py migrate`

### To run the application
`python manage.py runserver`

