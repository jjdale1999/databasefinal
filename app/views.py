"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
import os
from app import app, db
from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import CreateProfile,SignUp,Login,CreatePost,FriendType,Comment
# from app.models import UserProfile
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
import datetime

def format_date_joined(dat):
    return  dat.strftime("%B %d, %Y") 
###
# Routing for your application.
###


# all individual posts
@app.route('/posts')
def posts():
    # form=CreatePost()
    commentform=Comment()

#    getting both texts and images posts
    # posts=db.engine.execute("select * from (select * from texts union select * from  images)as allpost join posts on posts.postid= allpost.postid join profiles on posts.userid=profiles.userid")
    form=CreatePost()
    # posts=db.engine.execute("select * from (select * from texts union select * from  images)as allpost join posts on posts.postid= allpost.postid join profiles on posts.userid=profiles.userid")
    posts=db.engine.execute("select * from user_post_log join posts on posts.postid=user_post_log.postid join friendship on friendship.fuserid=user_post_log.userid join profiles on profiles.userid=user_post_log.userid  join gallery on profiles.profilepic=gallery.photoid where friendship.userid='"+session['userid']+"' order by posts.postid asc")
   
    # posts=db.engine.execute("select * from (select * from texts union select * from  images)as allpost join posts on posts.postid= allpost.postid join profiles on posts.userid=profiles.userid join friendship on friendship.fuserid=posts.userid where friendship.userid='"+session['userid']+"' order by posts.postid desc")
    # posts=db.engine.execute("select * from (select * from texts union select * from  images)as allpost join posts on posts.postid= allpost.postid join profiles on posts.userid=profiles.userid where posts.userid='"+userid+"' ")
    # posts=db.engine.execute("select * from (select * from texts union select * from  images)as allpost join posts on posts.postid= allpost.postid where posts.userid='"+userid+"'")
    return render_template('posts.html',commentform=commentform,posts=posts,form=form,profilepic=session['profilepic'],fname=session['fname'],username= session['username'],lname=session['lname'],email=session['email'],location=session['location'],biography=session['biography'],followers=session['followers'],following=session['following'],userid=session['userid'])

    # return render_template('posts.html',posts=posts,form=form,profilepic=session['profilepic'],fname=session['fname'],username= session['username'],lname=session['lname'],email=session['email'],location=session['location'],biography=session['biography'],followers=session['followers'],following=session['following'],userid=session['userid'])


@app.route('/grouplist')
def grouplist():
    
    groups=db.engine.execute("SELECT * FROM groups;")
    
    return render_template('grouplist.html', groups=groups,profilepic=session['profilepic'],fname=session['fname'],username= session['username'],lname=session['lname'],email=session['email'],location=session['location'],biography=session['biography'],followers=session['followers'],following=session['following'],userid=session['userid'])


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')

@app.route('/signup',methods=['POST', 'GET'])
def signup():
    createuser = SignUp()
    
    if request.method == "POST" and  createuser.validate_on_submit():
                fname = createuser.fname.data
                lname = createuser.lname.data
                email = createuser.email.data
                gender=createuser.gender.data
                password=createuser.password.data
                created_date=format_date_joined(datetime.datetime.now())
                 # get the last userid and then add it to one to get new userid
                # db.engine.execute("insert into Users (firstname,lastname,email,gender,password) values('"+firstname+"','"+lastname+"','"+email+"','"+gender+"','"+password+"')")


                return redirect(url_for('setupprofile'))
    else:
                flash_errors(createuser)
    return render_template('signup.html',form=createuser)  

@app.route('/friendlist/<userid>',methods=['GET'])
def friendlist(userid):
    friends=db.engine.execute("select * from friendship join users on users.userid=friendship.fuserid join profiles on profiles.userid=users.userid where friendship.userid='"+userid+"'")  
  
   
    return render_template('friendslist.html',friends=friends,profilepic=session['profilepic'],fname=session['fname'],username= session['username'],lname=session['lname'],email=session['email'],location=session['location'],biography=session['biography'],followers=session['followers'],following=session['following'],userid=session['userid'])


@app.route('/setupprofile',methods=['POST', 'GET'])
def setupprofile():
    createprofile = CreateProfile()
    
    if request.method == "POST" and  createprofile.validate_on_submit():
                username = createprofile.username.data
                location= createprofile.location.data
                biography=createprofile.biography.data
                photo= createprofile.profilepic.data
                created_date=format_date_joined(datetime.datetime.now())
                filename=secure_filename(photo.filename)
                photo.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                # db.engine.execute("insert into Profiles (userid,profilepic,username,biography,countryliving) values('"+str(userid)+"','"+profilepic+"','"+username+"','"+biography+"','"+country+"')")
		

                return redirect(url_for('posts'))
    else:
                flash_errors(createprofile)
    return render_template('setupprofile.html',form=createprofile)   

@app.route('/addfollower/<followerid>',methods=['POST'])
def addfollower(followerid):
    form=FriendType()
    friendtype = form.friendtype.data
    # print(friendtype)
    # db.engine.execute("insert into Friendship (userid,fuserid,ftype) values('"+str(session['userid'])+"','"+str(followerid)+"','"+friendtype+"')")
    return redirect(url_for('profile',userid=followerid))
@app.route('/createpost/<option>',methods=['POST', 'GET'])
def createpost(option):
    createpost = CreatePost()
    textpost=createpost.text.data
    postDate='2020-04-24'
    postTime='12:09:00'
    if request.method == "POST":
        # print("went into function")
        if(textpost!=""):
            print("textpost")
            db.engine.execute("insert into  posts(content,ctype, postDateTime) values('"+textpost+"','text','"+str(datetime.datetime.now())+"')")

        else:
            photo= createpost.image.data
                # created_date=format_date_joined(datetime.datetime.now())
            filename=secure_filename(photo.filename)
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            db.engine.execute("insert into gallery(photourl) values('"+'/static/uploads/'+filename+"')")
            lastphotoid= db.engine.execute("select photoid from gallery order by photoid desc limit 1")
            for last in lastphotoid:
                photoid=last.photoid
            db.engine.execute("insert into addphoto(photoid ,userid) values ('"+str(photoid)+"','"+session['userid']+"')")

            db.engine.execute("insert into  posts(content,ctype, postDateTime) values('"+'/static/uploads/'+filename+"','text','"+str(datetime.datetime.now())+"')")

        lastpostid= db.engine.execute("select postId from posts order by postid desc limit 1")
        for last in lastpostid:
            postId=last.postid
        db.engine.execute("insert into user_post_log(postid ,userid) values ('"+str(postId)+"','"+session['userid']+"')")

        return redirect(url_for('posts'))
   
    
@app.route('/setprofilepic/<path:image>')
def setprofilepic(image):
    setprofilepic=db.engine.execute("update profiles set profilepic='"+"/"+image+"' where userid="+session['userid'])
    print(image)
    if(image.startswith("static")):
        session['profilepic']="/"+image
    else:
         session['profilepic']=image
    return redirect(url_for('userposts',userid=session['userid']))
@app.route('/profile/<userid>')
def profile(userid):
    form=FriendType()
    commentform=Comment()
    users=db.engine.execute("select * from profiles join users on profiles.userid=users.userid join gallery on gallery.photoid=profiles.profilepic where users.userid='"+userid+"'")
    # posts=db.engine.execute("select * from (select * from texts union select * from  images)as allpost join posts on posts.postid= allpost.postid join profiles on posts.userid=profiles.userid  where posts.userid='"+str(userid)+"' order by posts.postid desc")
    posts=db.engine.execute("select * from user_post_log join posts on posts.postid=user_post_log.postid  join profiles on profiles.userid=user_post_log.userid  join gallery on profiles.profilepic=gallery.photoid where profiles.userid='"+str(userid)+"' order by posts.postid asc")

    return render_template('profilepage.html',commentform=commentform,fform=form,posts=posts,users=users,profilepic=session['profilepic'],fname=session['fname'],username= session['username'],lname=session['lname'],email=session['email'],location=session['location'],biography=session['biography'],followers=session['followers'],following=session['following'],userid=session['userid'])


# all individual posts for a specific user
@app.route('/posts/<userid>')
def userposts(userid):
    form=CreatePost()
    fform=FriendType()

    commentform=Comment()
    users=db.engine.execute("select * from profiles join users on profiles.userid=users.userid where users.userid='"+userid+"'")
    # posts=db.engine.execute("select * from (select * from texts union select * from  images)as allpost join posts on posts.postid= allpost.postid join profiles on posts.userid=profiles.userid  where posts.userid='"+str(userid)+"' order by posts.postid desc")
    posts=db.engine.execute("select * from user_post_log join posts on posts.postid=user_post_log.postid where posts.userid='"+str(userid)+"' order by posts.postid desc")
    # posts=db.engine.execute("select * from (select * from texts union select * from  images)as allpost join posts on posts.postid= allpost.postid join profiles on posts.userid=profiles.userid where posts.userid='"+userid+"' order by posts.postid desc")

    # posts=db.engine.execute("select * from (select * from texts union select * from  images)as allpost join posts on posts.postid= allpost.postid join profiles on posts.userid=profiles.userid where posts.userid='"+userid+"' ")
    # posts=db.engine.execute("select * from (select * from texts union select * from  images)as allpost join posts on posts.postid= allpost.postid where posts.userid='"+userid+"'")
    return render_template('profilepage.html',fform=fform,commentform=commentform,posts=posts,form=form,users=users,profilepic=session['profilepic'],fname=session['fname'],username= session['username'],lname=session['lname'],email=session['email'],location=session['location'],biography=session['biography'],followers=session['followers'],following=session['following'],userid=session['userid'])

    # return render_template('posts.html',form=form,posts=posts,comments=comments,profilepic=session['profilepic'],fname=session['fname'],username= session['username'],lname=session['lname'],email=session['email'],location=session['location'],biography=session['biography'],followers=session['followers'],following=session['following'],userid=session['userid'])
@app.route('/addcomment/<postid>',methods=['GET','POST'])
def addcomment(postid):
    print("adding comment")
    form=Comment()
    commentDetail=form.comment.data
    commentDate="2020/04/25"
    commentTime="2:24:08"
    # addcomments=db.engine.execute("insert into comments (postid,userid,commentdetail,commentdate,commenttime) values('"+str(postid)+"','"+str(session['userid'])+"','"+commentDetail+"','"+str(commentDate)+"','"+commentTime+"')")
    
# db.engine.execute("create table comments(commentId SERIAL,commentDetail varchar(255),commentDateTime timestamp,primary key (commentId) )")

# db.engine.execute("create table addcomments(commentId int,postId int,userid int,primary key(commentId,postId))")
# import datetime

# x = datetime.datetime.now()
    addcomments=db.engine.execute("insert into comments(commentdetail,commentdatetime) values('"+commentDetail+"','"+str(datetime.datetime.now())+"')")
    lastcommentid=db.engine.execute("select commentid from comments order by commentid desc limit 1")
    for x in lastcommentid:
        commentid=x.commentid
    db.engine.execute("insert into addcomments(commentid,postid,userid) values('"+str(commentid)+"','"+str(postid)+"','"+str(session['userid'])+"')")

    return redirect(url_for('posts'))
@app.route('/comments/<postid>')
def comments(postid):
    # comments=db.engine.execute("select * from comments where postid='"+str(postid)+"'")
    return render_template('comments.html',comments=comments)

@app.route('/')
@app.route('/login', methods=['POST', 'GET'])
def login():
    loginform=Login()
    if request.method == "POST" and  loginform.validate_on_submit():
        username=loginform.username.data
        password=loginform.password.data
        profile=db.engine.execute("select * from profiles join users on profiles.userid=users.userid where profiles.username='"+username+"' and password='"+password+"'")  
        print(profile.rowcount)
        if (profile.rowcount!=0):
            for y in profile:
                session['userid']=str(y.userid)
                session['fname']=y.firstname
                session['lname']=y.lastname
                session['email']=y.email
                session['username']=y.username
                session['location']=y.countryliving
                session['biography']=y.biography
                getprofilepic=db.engine.execute("select photourl from gallery where photoid="+str(y.profilepic))
                for m in getprofilepic:
                    session['profilepic']=m.photourl
            followings=db.engine.execute("select count(fuserid) as following from friendship where userid='"+str(session['userid'])+"'")   
            follower=db.engine.execute("select count(userid) as following from friendship where fuserid='"+str(session['userid'])+"'")  
            for x in followings:
                # print(x.following)
                session['following']=x.following
            for z in follower:
                session['followers']=z.following
            return redirect('posts')
        else:
            flash('Username or Password is incorrect.','danger')
    return render_template('login.html',form=loginform)

@app.route('/logout')
def logout():
    flash("Logged out successfully!!!","success")
    loginform=Login()
    return redirect('login')

# Flash errors from the form if validation fails
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
