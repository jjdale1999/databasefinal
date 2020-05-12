from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import psycopg2

from flask import render_template
app = Flask(__name__)
SQLALCHEMY_DATABASE_URI ="postgresql://project2:project2@localhost/project2"
SQLALCHEMY_TRACK_MODIFICATIONS = False
UPLOAD_FOLDER = "./app/static/uploads"
SECRET_KEY = 'Sup3r$3cretkey'
app.config.from_object(__name__)



db = SQLAlchemy(app)

conn = psycopg2.connect("dbname=project2 user=project2 password=project2")
cur = conn.cursor()



def comments(postid):
    # comments=db.engine.execute("select addcomments.postid as postid,profiles.username as username,gallery.photourl as photourl,addcomments.userid as userid,commentdetail from addcomments join profiles on profiles.userid=addcomments.userid join comments on addcomments.commentid=comments.commentid join gallery on profiles.profilepic=gallery.photoid where addcomments.postid="+str(postid))
    comments=db.engine.execute("select allcomment.postid as postid,profiles.username as username,gallery.photourl as photourl,allcomment.userid as userid,commentdetail from profiles join ((select * from addcomments where postid="+str(postid)+")As addcomment join comments on comments.commentid=addcomment.commentid)as allcomment on profiles.userid=allcomment.userid join gallery on profiles.profilepic=gallery.photoid")

    return comments
app.jinja_env.globals.update(comments=comments)

def getgallery(userid):
    getgallery=db.engine.execute("select * from addphoto join gallery on gallery.photoid=addphoto.photoid where userid="+str(userid) +"order by gallery.photoid desc")
    return getgallery

app.jinja_env.globals.update(getgallery=getgallery)


def getlikes(postid,userid):
    length=0
    getlikes=db.engine.execute("select userid from likes where postid="+str(postid)+"and userid="+str(userid))
    for x in getlikes:
        length=1
    return length
app.jinja_env.globals.update(getlikes=getlikes)


def getlikescount(postid):
    countid=0
    getlikescount=db.engine.execute("select count(userid) as countid from likes where postid="+str(postid))
    for x in getlikescount:
        countid=x.countid
    return countid
app.jinja_env.globals.update(getlikescount=getlikescount)


def getfrienship(userid,friendid):
    length=0
    getfrienship=db.engine.execute("select * from friendship where userid="+str(userid)+" and fuserid="+str(friendid))
    for x in getfrienship:
        length=1
    return length
app.jinja_env.globals.update(getfrienship=getfrienship)

#     setprofilepic=db.engine.execute("update profiles set profilepic='"+image+"' where userid="+str(userid))
#     return ""
# app.jinja_env.globals.update(setprofilepic=setprofilepic)

from app import views
