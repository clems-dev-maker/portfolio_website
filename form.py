from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SubmitField, DateField, FileField, IntegerField
from wtforms.validators import DataRequired


# create a form to add projects with Flask-WTF
class ProjectForm(FlaskForm):
    project_name = StringField('Project Name', validators=[DataRequired()])
    project_description = StringField('Project Description', validators=[DataRequired()])
    project_link = StringField('Project Link', validators=[DataRequired()])
    image_file = FileField('Project Image', validators=[FileAllowed(['jpg', 'png'])])
    date_field = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    submit = SubmitField('Add Project')


class EditProjectForm(FlaskForm):
    project_name = StringField('Project Name', validators=[DataRequired()])
    project_description = StringField('Project Description', validators=[DataRequired()])
    project_link = StringField('Project Link', validators=[DataRequired()])
    image_file = FileField('Project Image', validators=[FileAllowed(['jpg', 'png'])])
    date_field = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    submit = SubmitField('Edit Project')


# create a form to log in with Flask-WTF
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


# create a form to sign up with Flask-WTF
class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')


# create a contact form with Flask-WTF
class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    message = StringField('Message', validators=[DataRequired()])
    submit = SubmitField('Send Message')


# create a form to add comments with Flask-WTF
class CommentForm(FlaskForm):
    author = StringField('Author', validators=[DataRequired()])
    comment_text = StringField('Comment', validators=[DataRequired()])
    submit = SubmitField('Add Comment')
