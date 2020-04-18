from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
SQLALCHEMY_DATABASE_URI ="postgresql://project1:project1@localhost/project1"
SQLALCHEMY_TRACK_MODIFICATIONS = False
UPLOAD_FOLDER = "./app/static/uploads"
SECRET_KEY = 'Sup3r$3cretkey'
app.config.from_object(__name__)

db = SQLAlchemy(app)

from app import views
