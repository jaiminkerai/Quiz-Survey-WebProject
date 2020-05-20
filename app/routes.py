'''
Decorators which allows us to write a function that 
returns the information displayed on the website for a specific route. 
'''
from flask import render_template, flash, redirect, url_for, abort
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user
from app.models import User
from flask_login import logout_user, LoginManager
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse
from app import db  
from app import login
from app.forms import RegistrationForm
from datetime import datetime
from app.forms import EditProfileForm
from app.forms import PostForm
from app.forms import AnswerForm
from app.models import Post
from app.forms import ResetPasswordRequestForm
from app.email import send_password_reset_email
from app.forms import ResetPasswordForm
from app.models import Quizzes
from app.models import Questions
from app.models import ADMINS
from app.models import quizMarks
from app.models import ADMINS
from app.models import multiChoice
from app.models import LongQuestions
from app.models import load_user
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
from flask import g


@app.route('/', methods=['GET', 'POST']) 
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    # For posting comments 1-140 characters long
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!', 'alertSuccess')
        return redirect(url_for('index'))
    
    # Get current user's posts
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title='Home', form=form,
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        # If user does not exist or the password is incorrect, redirect back to login
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', category='alertError')
            return redirect(url_for('login'))

        # Log the user in
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next') # If next page exists, get it

        # If there is not a next page, redirect to the home page 
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')

        # Redirect to the next page
        return redirect(next_page)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    # If current user is logged in, redirect to the home page
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()

    # After clicking the submit button: 
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!','alertSuccess') # A one time message
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('user.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        g.user = load_user(current_user.id)
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)

    # Change current user fields based on form input post
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.', 'alertSuccess')
        return redirect(url_for('edit_profile'))
    
    # Show current account details
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)

# Follow and unfollow routes.
@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username), 'alertError')
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot follow yourself!', 'alertError')
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(username), 'alertSuccess')
    return redirect(url_for('user', username=username))

@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username), 'alertError')
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot unfollow yourself!', 'alertError')
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(username), 'alertError')
    return redirect(url_for('user', username=username))

@app.route('/explore')
@login_required
def explore():
    # Get all user's posts
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('explore', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template("index.html", title='Explore', posts=posts.items,
                          next_url=next_url, prev_url=prev_url)

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password', 'alertInfo')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)
    
@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.', 'alertSuccess')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)

@app.route('/quizzes')
def quizzes():
    # Find all the quizzes
    page = request.args.get('page', 1, type=int)
    quizzes = Quizzes.query.order_by(Quizzes.pub_date.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
    
    return render_template("quiz.html", title='Explore', quizzes=quizzes.items)

@app.route('/assessments/<username>')
@login_required
def assessments(username):
    if username != current_user.username:
        abort(403)

    # Get the user object
    user = User.query.filter_by(username=username).first_or_404()

    # For pagination, start page
    page = request.args.get('page', 1, type=int)
    
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)

    # quizMarks iterable for the specific user
    quizzes = user.marksOf.paginate(page, app.config['POSTS_PER_PAGE'], False)

    # Links that allow users to navigate to the next or previous page
    next_url = url_for('assessments', page=quizzes.next_num) \
        if quizzes.has_next else None
    prev_url = url_for('assessments', page=quizzes.prev_num) \
        if quizzes.has_prev else None

    return render_template('assessments.html', user=user, posts=posts.items, quizzes=quizzes.items)

@app.route('/quizzes/<quizname>/<quizid>')
@login_required
def quizform(quizname, quizid):
    # Get Quiz by ID and adding multiple choice options
    form = AnswerForm()
    radio = multiChoice.query.filter_by(quiz_id=quizid).first_or_404()
    form.options.choices = [radio.choice1, radio.choice2, radio.choice3, radio.choice4]
    quiz = Quizzes.query.filter_by(id=quizid).first_or_404()
    page = request.args.get('page', 1, type=int)

    # Find Short Answer and MCQ
    worded = quiz.questions.paginate(page)
    MCQ = quiz.mcquestion.paginate(page)
    longworded = quiz.longquestions.paginate(page)

    # Submitting Validation
    
    return render_template('quiz_questions.html', quiz=quiz, worded=worded.items, MCQ=MCQ.items, longworded=longworded.items,form=form)

# Overrides the Flask_Admin Classes to authenticate users before accessing the admin terminal
class MyModelView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated:
            user = load_user(current_user.id)
            return user.isAdmin()
        return current_user.is_authenticated
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))
 
class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated:
            user = load_user(current_user.id)
            return user.isAdmin()
        return current_user.is_authenticated
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))

admin = Admin(app, index_view=MyAdminIndexView())

admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Quizzes, db.session))
admin.add_view(MyModelView(Questions, db.session))
admin.add_view(MyModelView(multiChoice, db.session))
admin.add_view(MyModelView(LongQuestions, db.session))
admin.add_view(MyModelView(quizMarks, db.session))
admin.add_link(MenuLink(name='Back to Website', category='', url='/'))