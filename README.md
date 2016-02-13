Instructions for running Project locally:
	1. Open in Command Prompt the file repository
	2. Type 'python manage.py runserver'
	3. Navigate to '127.0.0.1:8000'

If you are missing requirements, run the following line in Command Prompt in order to install all requirements from requirements.txt
	pip install -r requirements.txt



Admin panel is available at '127.0.0.1:8000/admin'
In order to reset the database, run (in Command Prompt):
	python manage.py reset_db
	python manage.py syncdb
Follow prompts to create superuser and record the username and password
	python manage.py runserver

