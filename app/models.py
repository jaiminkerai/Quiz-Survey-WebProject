from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db
from flask_login import UserMixin
from app import login
from hashlib import md5
from time import time
import jwt
from app import app

ADMINS = ['cits3403test@gmail.com']

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    authorOf = db.relationship('Quizzes', backref='author', lazy='dynamic')
    
    admin = db.Column(db.Boolean, unique=False, default=False)

    marksOf = db.relationship('quizMarks', backref='markOf', lazy='dynamic')
    longanswers = db.relationship('LongAnswers', backref='user', lazy='dynamic')

    def isAdmin(self):
        return self.admin

    def doneQuiz(self, quizid):
        quiz_done = quizMarks.query.filter_by(quiz_id=quizid,user_id=self.id).count()
        return quiz_done == 0

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '{}'.format(self.username)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')
    


    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'))

    def __repr__(self):
        return 'Post: {}'.format(self.body)

# Reloading the user from the user id stored in a session
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

#databases for quizes and questions

class Quizzes(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(255))
    # Connected to user for now
    questions = db.relationship('Questions', backref='Quizzes', lazy='dynamic')
    mcquestion = db.relationship('multiChoice', backref='MCQuizzes', lazy='dynamic')
    longquestions = db.relationship('LongQuestions', backref='LongQuizzes', lazy='dynamic')
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    pub_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    quizMarks = db.relationship('quizMarks', backref='quizMarks', lazy='dynamic')
    posts= db.relationship('Post', backref='Quiz', lazy='dynamic')

    def __repr__(self):
        return 'Quiz: {}'.format(self.name)  
    
class Questions(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    question = db.Column(db.String(255))
    solution = db.Column(db.String(255))
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'))

    def __repr__(self):
        return 'Question: {}'.format(self.question)

class LongQuestions(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    question = db.Column(db.String(500))
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'))
    lanswers = db.relationship('LongAnswers', backref='Question', lazy='dynamic')

    def __repr__(self):
        quizfrom = Quizzes.query.filter_by(id=self.quiz_id).first()
        return '{}, L-Question {}'.format(quizfrom , self.question)

class LongAnswers(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement=True, unique=True)
    answer = db.Column(db.String(500))
    longquestion_id = db.Column(db.Integer, db.ForeignKey('long_questions.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        user = User.query.filter_by(id=self.user_id).first()
        return 'L-Answer: {}'.format(user)

class quizMarks(db.Model):
    quizMarks_id = db.Column(db.Integer, primary_key = True, autoincrement=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'))
    mark = db.Column(db.Float)
    feedback = db.Column(db.String(500))

def __repr__(self):
        return 'Marks: {}'.format(self.user_id)

class multiChoice(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'))
    question = db.Column(db.String(128), unique=False, nullable=False)
    choice1 = db.Column(db.String(128), unique=False, nullable=False)
    choice2 = db.Column(db.String(128), unique=False, nullable=False)
    choice3 = db.Column(db.String(128), unique=False, nullable=False)
    choice4 = db.Column(db.String(128), unique=False, nullable=False)
    correct = db.Column(db.String(128), unique=False, nullable=False)
    
    def __repr__(self):
        return "MCQuestion {}>".format(self.question)
        return "< Quiz {} question: {}  {} {} {} {} {} {} >".format(
            self.question,
            self.choice1,
            self.choice2,
            self.choice3,
            self.choice4,
            self.correct
        )

