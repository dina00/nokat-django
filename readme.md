# nokat-django :joy_cat:

## Overview
This project consists of sharing a feed of jokes (nokat) where a user can post their own jokes, up vote/down vote other jokes or comment on them.

## How to run the project
- In you code editor's terminal run the following:
1. It is better to create a [virtual](https://docs.python.org/3/library/venv.html) environment.
2. Install the requirements through `pip install -r requirements.txt`.
3. Navigate into the project's directory `cd nokat_project`.
4. Migrate the database `python manage.py migrate` and `python manage.py makemigrations `.
5. Create a  super user to access the Django admin interface
 `python manage.py createsuperuser`.
6.  Run the project 
`python manage.py runserver`.
7. Type [http://localhost:8000](http://localhost:8000) into your browser's address bar and hit enter.
### Note 
- Make sure to clear your cache so that the static file can load properly.