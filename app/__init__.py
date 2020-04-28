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
    # comments=db.engine.execute("select addcomments.postid as postid,profiles.username as username,gallery.photourl as photourl,addcomments.userid as userid,commentdetail from addcomments join profiles on profiles.userid=addcomments.userid join comments on addcomments.commentid=comments.commentid join gallery on profiles.profilepic=gallery.photoid where addcomments.postid="+str(postid))
    comments=db.engine.execute("select allcomment.postid as postid,profiles.username as username,gallery.photourl as photourl,allcomment.userid as userid,commentdetail from profiles join ((select * from addcomments where postid="+str(postid)+")As addcomment join comments on comments.commentid=addcomment.commentid)as allcomment on profiles.userid=allcomment.userid join gallery on profiles.profilepic=gallery.photoid")

    return comments
app.jinja_env.globals.update(comments=comments)

def getgallery(userid):
    getgallery=db.engine.execute("select * from addphoto join gallery on gallery.photoid=addphoto.photoid where userid="+str(2) +"order by gallery.photoid")
    return getgallery

app.jinja_env.globals.update(getgallery=getgallery)



#     setprofilepic=db.engine.execute("update profiles set profilepic='"+image+"' where userid="+str(userid))
#     return ""
# app.jinja_env.globals.update(setprofilepic=setprofilepic)

from app import views
