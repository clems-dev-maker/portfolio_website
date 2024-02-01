import os
from datetime import datetime
from functools import wraps

import flask
from django.utils.http import url_has_allowed_host_and_scheme
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor
from flask_bootstrap import Bootstrap5
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

from form import ProjectForm, ContactForm, LoginForm, EditProjectForm, CommentForm, SignupForm

# create an instance of Flask
app = Flask(__name__, static_url_path='/static')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
ckeditor = CKEditor(app)
db = SQLAlchemy(app)
app.config["SECRET_KEY"] = "djdksjklsjdl"
bootstrap = Bootstrap5(app)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    user = User.query.filter_by(user_id=user_id).first()
    if user:
        return user
    return None


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return decorated_function


# admin only decorator
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.user_id != 1:
            return redirect(url_for("home"))
        return f(*args, **kwargs)

    return decorated_function


# create a model for the database
class Project(db.Model):
    # create columns in the database
    project_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)  # nullable = False means it has to have a title
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default='N/A')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # print out the id when a project is created
    def __repr__(self):
        return 'Project ' + str(self.project_id)


# create a class for the user
class User(db.Model, UserMixin):
    # create columns in the database
    user_id = db.Column(db.Integer, db.ForeignKey('message.message_id'), primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)  # nullable = False means it has to have a title
    email = db.Column(db.String(100), nullable=False)
    login = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100), nullable=False)

    # print out the id when a project is created
    def __repr__(self):
        return 'User ' + str(self.user_id)

    # flask login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    def __unicode__(self):
        return self.username


# create a class for the contact form
class Message(db.Model):
    # create columns in the database
    message_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # nullable = False means it has to have a title
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)

    # print out the id when a project is created
    def __repr__(self):
        return 'Message ' + str(self.message_id)


class Comments(db.Model):
    # create columns in the database
    author_id = db.Column(db.Integer, db.ForeignKey('message.message_id'), primary_key=True)
    comment_author = db.Column(db.String(100), nullable=False)  # nullable = False means it has to have a title
    comment_id = db.Column(db.Integer, primary_key=True)
    comment_text = db.Column(db.Text, nullable=False)

    # print out the id when a project is created
    def __repr__(self):
        return 'Comment ' + str(self.comment_id)


# create all the datrabase tables
with app.app_context():
    db.create_all()


# create a route for the home page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        new_username = request.form['username']
        new_password = request.form['password']
        user = User.query.filter_by(username=new_username).first()
        if user is None:
            new_user = User(username=new_username, password=new_password)
            db.session.add(new_user)
            db.session.commit()
            login_user(user)
        else:
            projects = Project.query.order_by(Project.title).all()
            return render_template('index.html', projects=projects, new_username=new_username)
    else:
        projects = Project.query.order_by(Project.title).all()
        return render_template('index.html', projects=projects)


# create a route for the about page
@app.route('/about', methods=['GET', 'POST'])
def about():
    name = 'Clément Cathala'
    job = "I'm a web developer"
    form = CommentForm()
    if form.validate_on_submit():
        # get the data from the form
        author_id = form.author.data
        comment_author = form.author.data
        comment_id = form.comment_text.data
        comment_text = form.comment_text.data
        # create a new comment
        new_comment = Comments(
            comment_text=comment_text,
            comment_author=comment_author,
            author_id=author_id,
            comment_id=comment_id
        )
        # add the new comment to the database
        db.session.add(new_comment)
        # commit the changes to the database
        db.session.commit()
        # redirect to the about page
        return redirect(url_for('about'))
    # create a list of dictionary about programming languages
    programming_languages = [{'language1': 'Python',
                              'language2': 'JavaScript',
                              'language3': 'HTML',
                              'language4': 'CSS',
                              'language5': 'Flask',
                              'language6': 'Django'}]
    return render_template('about.html', name=name, job=job, form=form, comments=Comments.query.all(),
                           programming_languages=programming_languages)


# create a route for the contact page from the ContactForm
@app.route('/contact/', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if ContactForm.validate_on_submit(form):
        # get the data from the form
        name = form.name.data
        email = form.email.data
        message = form.message.data
        # create a new message
        new_message = Message(name=name, email=email, message=message)
        # add the new message to the database
        db.session.add(new_message)
        # commit the changes to the database
        db.session.commit()
        # redirect to the contact page
        return redirect(url_for('about'))
    else:
        return render_template('contact.html', form=form)



@admin_only
@app.route('/add/', methods=['GET', 'POST'])
def add_project():
    form = ProjectForm()
    if ProjectForm.validate_on_submit(form):
        # get the data from the form
        title = form.project_name.data
        content = form.project_description.data
        author = form.author.data
        # create a new project
        new_project = Project(title=title, content=content, author=author)
        # add the new project to the database
        db.session.add(new_project)
        # commit the changes to the database
        db.session.commit()
        # redirect to the portfolio page
        return redirect(url_for('index'))
    else:
        # get all the projects from the database
        all_projects = Project.query.order_by(Project.title).all()
        return render_template('add_project.html', projects=all_projects, form=form)


@admin_only
@app.route('/edit/<int:project_id>', methods=['GET', 'POST'])
def edit_project(project_id):
    form = EditProjectForm()
    project = Project.query.get_or_404(project_id)
    # if the request method is POST, then get the data from the form
    if ProjectForm.validate_on_submit(form):
        # get the data from the form
        project.title = form.project_name.data
        project.content = form.project_description.data
        project.author = form.author.data  # nullable = False means it has to have a title
        # commit the changes to the database
        db.session.commit()
        # redirect to the portfolio page
        return redirect(url_for('index'))
    else:
        # get all the projects from the database
        all_projects = Project.query.order_by(Project.title).all()
        return render_template('edit_project.html', projects=all_projects, project_id=project, form=form)


@admin_only
@app.route('/delete/<int:project_id>')
def delete_project(project_id):
    # get the project from the database
    project = Project.query.get_or_404(project_id)
    # delete the project from the database
    db.session.delete(project)
    # commit the changes to the database
    db.session.commit()
    # redirect to the portfolio page
    return redirect(url_for('index'))


# create a route to sign up
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if SignupForm.validate_on_submit(form):
        # get the data from the form
        username = form.username.data
        email = form.email.data
        password = form.password.data
        # create a new user
        new_user = User(username=username, email=email, password=password)
        # add the new user to the database
        db.session.add(new_user)
        # commit the changes to the database
        db.session.commit()
        # redirect to the portfolio page
        return redirect(url_for('index'))
    return render_template('signup.html', form=form)


# create a route to login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # get the user from the database
        user = User.query.filter_by(username=form.username.data).first()
        # check if the user exists
        if user:
            # check if the password is correct
            if user.password == form.password.data:
                login_user(user)
                return redirect(url_for("index"))

            else:
                return render_template("login.html", form=form, error="Password is incorrect or user does not exist")
    return render_template("login.html", form=form)


# create a route to logout
@login_required
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


# run the app
if __name__ == '__main__':
    app.run(debug=True)
