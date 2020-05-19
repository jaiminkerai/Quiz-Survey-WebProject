'''Runs the application'''
from app import app # From app folder __init__.py file import app variable
from app.models import User, Post, db, Quizzes, Questions

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Quizzes': Quizzes, 'Questions': Questions, 'quizMarks': quizMarks, 'multiChoice': multiChoice}