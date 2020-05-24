# Quizards

Quizards is a teacher-student web-based quiz application created through Flask.

## Purpose

- To allow teachers to create quizzes that involve multiple-choice, short answer and/or long answer questions which are easily accessible by students
- Quizards acts as a platform for Educational Assessments and utilises several assessment mechanisms including: multiple-choice, short answer with fuzzy matching and manual assessment of long answers

## Architecture

``` GAP
├─ app/         # All application code in this directory.         
│  ├─ static/   # Static folder for CSS and JavaScript
│  │  ├─ scripts.js   # JavaScript file
│  │  └─ css/    # CSS files for all pages
│  │     ├─ styles.css
│  │     └─ templogo.png
│  │         
│  ├─ templates/      # HTML templates used/included throughout the app.
│  │  ├─ admin/
│  │  │    └─ index.html
│  │  ├─ email/            
│  │  │    ├─ reset_password.html
│  │  │    └─ reset_password.txt  
│  │  |
│  │  ├─ _post.html
│  │  ├─ 403.html
│  │  ├─ 404.html
│  │  ├─ 500.html
│  │  ├─ assessments.html
│  │  ├─ base.html
│  │  ├─ edit_profile.html
│  │  ├─ index.html
│  │  ├─ login.html
│  │  ├─ quiz_questions.html
│  │  ├─ quiz.html
│  │  ├─ quizdisplay.html
│  │  ├─ register.html
│  │  ├─ reset_password_request.html
│  │  ├─ reset_password.html
│  │  ├─ scores.html
│  │  ├─ tutorial.html
│  │  └─ user.html
│  ├─ __init__.py
│  ├─ email.py   
│  ├─ errors.py     
│  ├─ forms.py 
|  ├─ models.py
│  └─ routes.py  
│
├─ logs/   # Logs errors
├─ requirements.txt # Text file with all necessary dependencies
├─ config.py 
├─ geckodriver.exe   # Geckodriver for selenium tests 
├─ app.db   # Database of Quizards
├─ .gitignore   # Ignores any files in this text file
├─ system.py     # Selenium testing for login feature
└─ tests.py      # Unit testing for User Model
```
### Getting Started

These instructions will allow you to run the quiz application on your local machine for development and testing purposes

#### Prerequisites

- Python(tested with version 3.8.3)
- SQLAlchemy(tested with version 1.3.16)
- SQLite3
- FireFox 
- Geckodriver

#### Installing
1. Clone this repository
```
	$ git clone http://github.com/jaiminkerai/CITS3403Project2
	$ cd CITS3403Project2
```

2. Create a virtualenv, and activate this: 
```
	$ python3 -m venv venv
	$ . venv/bin/activate
```

3. Install all necessary dependencies:
```
	$ pip install -r requirements.txt
```

4. Exporting the FLASK_APP environment variable:
```
	$ export FLASK_APP = CITS3403-PROJECT2.py
```

5. Run the application:
```
	$ flask run
```
6. To access the Quizards application, visit:
```
	http://localhost:5000
```
	  
## Tests
### Unit Tests
To run the unit tests covering Quizard's User Model:

	$ python3 tests.py
	
### Selenium Test
#### Disclaimer:
- Firefox must be installed
- The original database will be overridden so to restore it, the changes to app.db must be deleted before committing

To run the selenium test covering Quizard's Login feature:

    $ python3 system.py
	
## Contributions

To see the commit logs visit the commits.txt file

### Contributors:
![Screenshot (113)](https://user-images.githubusercontent.com/64474462/82753954-60d34780-9dfc-11ea-9e4c-eeaab56fc643.png)




