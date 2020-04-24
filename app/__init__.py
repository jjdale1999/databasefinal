from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

from flask import render_template
app = Flask(__name__)
SQLALCHEMY_DATABASE_URI ="postgresql://project2:project2@localhost/project2"
SQLALCHEMY_TRACK_MODIFICATIONS = False
UPLOAD_FOLDER = "./app/static/uploads"
SECRET_KEY = 'Sup3r$3cretkey'
app.config.from_object(__name__)



db = SQLAlchemy(app)


def comments(postid):
    comments=db.engine.execute("select * from comments join profiles on comments.userid=profiles.userid where postid='"+postid+"'")
    return comments
app.jinja_env.globals.update(comments=comments)

from app import views
