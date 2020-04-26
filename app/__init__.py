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
    comments=db.engine.execute("select addcomments.postid as postid,profiles.username as username,gallery.photourl as photourl,addcomments.userid as userid,commentdetail from addcomments join profiles on profiles.userid=addcomments.userid join comments on addcomments.commentid=comments.commentid join gallery on profiles.profilepic=gallery.photoid where addcomments.postid="+str(postid))
    
    return comments
app.jinja_env.globals.update(comments=comments)


def addcomments(postid,cuserid,commmentDetail,commentDate,commentTime):
    addcomments=db.engine.execute("insert into comments (postid,userid,commentdetail,commentdate,commenttime) values('"+str(postId)+"','"+str(cuserid)+"','"+commmentDetail+"','"+str(commentDate)+"','"+commentTime+"')")
    return ""
app.jinja_env.globals.update(addcomments=addcomments)

# def setprofilepic(image,userid):
#     setprofilepic=db.engine.execute("update profiles set profilepic='"+image+"' where userid="+str(userid))
#     return ""
# app.jinja_env.globals.update(setprofilepic=setprofilepic)

from app import views
