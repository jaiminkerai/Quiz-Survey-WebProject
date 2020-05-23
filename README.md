# Quizards

Quizards is a teacher-student web-based quiz application created through Flask.

## Purpose

To allow teachers to create quizzes that involve multiple-choice, short answer and/or long answer questions which are easily accessible by students. 

### Getting Started

These instructions will allow you to run the quiz application on your local machine for development and testing purposes

#### Prerequisites

- Python(tested with version 3.8.3)
- SQLAlchemy(tested with version 1.3.16)

#### Installing
Assuming use of cmd:
1. Clone this repository
    $ git clone http://github.com/jaiminkerai/CITS3403Project2
    $ cd CITS3403Project2

2. Create a virtualenv, and activate this: 

    $ virtualenv env 
    $ source env/bin/activate

3. Install all necessary dependencies:

    $ pip install -r requirements.txt

4. Run the application:

	  $ flask run

5. To access the Quizards application, visit:

	  http://localhost:5000
	  
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
	
## Commit Logs




