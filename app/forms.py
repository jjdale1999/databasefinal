from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField,TextAreaField,SelectField
from wtforms.validators import DataRequired, Email

from wtforms import PasswordField
from wtforms.validators import InputRequired
class CreateProfile(FlaskForm):
    fname = StringField('First Name', validators=[DataRequired()],render_kw={"placeholder":"Jane"})
    lname = StringField('Last Name', validators=[DataRequired()],render_kw={"placeholder":"Doe"})
    email = StringField('Email', validators=[DataRequired(), Email()],render_kw={"placeholder":"eg. jdoe@example.com"})
    location = StringField('Location', validators=[DataRequired()],render_kw={"placeholder":"eg. Kingston,Jamaica"})
    gender = SelectField('Gender',choices=[('Male','Male'),('Female','Female')])
    biography = TextAreaField('Biography',validators=[DataRequired()])
    photo = FileField('Photo',validators=[FileRequired(),FileAllowed(['jpg','jpeg','png','Images Only'])])



