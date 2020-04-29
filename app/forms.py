from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField,TextAreaField,SelectField,PasswordField
from wtforms.validators import DataRequired, Email

from wtforms import PasswordField
from wtforms.validators import InputRequired
class SignUp(FlaskForm):
    fname = StringField('First Name', validators=[DataRequired()],render_kw={"placeholder":"Jane"})
    lname = StringField('Last Name', validators=[DataRequired()],render_kw={"placeholder":"Doe"})
    email = StringField('Email', validators=[DataRequired(), Email()],render_kw={"placeholder":"eg. jdoe@example.com"})
    gender = SelectField('Gender',choices=[('Male','Male'),('Female','Female')])
    password = PasswordField('Password',validators=[DataRequired()])
    repassword = PasswordField('Re-Type Password',validators=[DataRequired()])


class CreateProfile(FlaskForm):
    username = StringField('Username', validators=[DataRequired()],render_kw={"placeholder":"janedoe123"})
    location = StringField('Location', validators=[DataRequired()],render_kw={"placeholder":"eg. Kingston,Jamaica"})
    biography = TextAreaField('Biography',validators=[DataRequired()])
    profilepic = FileField('Profile Pic',validators=[FileRequired(),FileAllowed(['jpg','jpeg','png','Images Only'])])



class CreatePost(FlaskForm):
    text = TextAreaField('Content',validators=[DataRequired()])
    image = FileField('Profile Pic',validators=[FileRequired(),FileAllowed(['jpg','jpeg','png','Images Only'])])

class Login(FlaskForm):
    username = StringField('Username', validators=[DataRequired()],render_kw={"placeholder":"Jane"})
    password = PasswordField('Password',validators=[DataRequired()])


class FriendType(FlaskForm):
    friendtype = SelectField('Relationship Type',choices=[('Relatives','Relatives'),('School','School'),('Work','Work')])


class Comment(FlaskForm):
        comment = StringField('Comment', validators=[DataRequired()],render_kw={"placeholder":"Add a Comment"})

class UploadProfilePic(FlaskForm):
    profilepic = FileField('Profile Pic',validators=[FileRequired(),FileAllowed(['jpg','jpeg','png','Images Only'])])


class SearchForm(FlaskForm):
        username = StringField('Username', validators=[DataRequired()],render_kw={"placeholder":"Username"})
