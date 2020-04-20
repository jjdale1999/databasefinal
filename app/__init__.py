from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
SQLALCHEMY_DATABASE_URI ="postgresql://project2:project2@localhost/project2"
SQLALCHEMY_TRACK_MODIFICATIONS = False
UPLOAD_FOLDER = "./app/static/uploads"
SECRET_KEY = 'Sup3r$3cretkey'
app.config.from_object(__name__)

db = SQLAlchemy(app)

from app import views
