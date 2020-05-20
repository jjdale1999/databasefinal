"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application."""

import os
from app import app, db,cur,conn
from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import CreateProfile,SignUp,Login,CreatePost,FriendType,Comment,UploadProfilePic,SearchForm, CreateGroupForm,EditProfile
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


    form=CreatePost()
  
    posts=db.engine.execute("select * from user_post_log inner join posts on posts.postid=user_post_log.postid inner join friendship on friendship.fuserid=user_post_log.userid inner join profiles on profiles.userid=user_post_log.userid  inner join gallery on profiles.profilepic=gallery.photoid where friendship.userid="+session['userid']+"order by posts.postid desc")
    uploadform=UploadProfilePic()

    
    return render_template('posts.html',editprofile=EditProfile(),searchform=SearchForm(), uploadform=uploadform,commentform=commentform,posts=posts,form=form,profilepic=session['profilepic'],fname=session['fname'],username= session['username'],lname=session['lname'],email=session['email'],location=session['location'],biography=session['biography'],followers=session['followers'],following=session['following'],userid=session['userid'])

    # return render_template('posts.html',posts=posts,form=form,profilepic=session['profilepic'],fname=session['fname'],username= session['username'],lname=session['lname'],email=session['email'],location=session['location'],biography=session['biography'],followers=session['followers'],following=session['following'],userid=session['userid'])


@app.route('/likepost/<postid>/<userid>',methods=['post','get'])
def likepost(postid,userid):
    cur.execute("CALL addlike("+str(postid)+","+str(userid)+")")
    conn.commit()
    return redirect(url_for('posts'))

@app.route('/unlikepost/<postid>/<userid>',methods=['post','get'])
def unlikepost(postid,userid):
    db.engine.execute("delete from likes where postid="+str(postid)+" and userid="+str(userid))
    return redirect(url_for('posts'))

@app.route('/grouplist')
def grouplist():
    
    groups=db.engine.execute("SELECT * FROM groups;")
    uploadform=UploadProfilePic()

    return render_template('grouplist.html',editprofile=EditProfile(),searchform=SearchForm(), uploadform=uploadform, groups=groups,profilepic=session['profilepic'],fname=session['fname'],username= session['username'],lname=session['lname'],email=session['email'],location=session['location'],biography=session['biography'],followers=session['followers'],following=session['following'],userid=session['userid'])

@app.route('/mygroups')
def mygroups():
    createGroupForm = CreateGroupForm()
    userid=session['userid']
    groups=db.engine.execute("SELECT g.groupid, groupname, createdby, createddate FROM groups g INNER JOIN joinsgroup jg ON g.groupid = jg.groupid WHERE userid = '"+userid+"';")
    uploadform=UploadProfilePic()

    
    return render_template('mygroups.html',editprofile=EditProfile(),searchform=SearchForm(), uploadform=uploadform, createGroupForm=createGroupForm, groups=groups,profilepic=session['profilepic'],fname=session['fname'],username= session['username'],lname=session['lname'],email=session['email'],location=session['location'],biography=session['biography'],followers=session['followers'],following=session['following'],userid=session['userid'])

@app.route('/creategroup', methods=['POST','GET'])
def creategroup():
    createGroupForm = CreateGroupForm()
    userid=session['userid']
    groups=db.engine.execute("SELECT g.groupid, groupname, createdby, createddate FROM groups g INNER JOIN joinsgroup jg ON g.groupid = jg.groupid WHERE userid = '"+userid+"';")
    uploadform=UploadProfilePic()

    if request.method == "POST":
        groupname = createGroupForm.groupname.data
        time = datetime.datetime.now()
        time = time.strftime("%Y-%m-%d %H:%M:%S")
        db.engine.execute("INSERT INTO  groups(groupname,createdby, createddate) values('"+groupname+"','"+str(userid)+"','"+time+"');")
        lastGroupID= db.engine.execute("SELECT groupid FROM groups ORDER BY groupid DESC LIMIT 1")
        for last in lastGroupID:
            groupid=last.groupid

        time = datetime.datetime.now()
        time = time.strftime("%Y-%m-%d %H:%M:%S")
        db.engine.execute("INSERT INTO joinsGroup (groupid,userid,status,joindate) values('"+str(groupid)+"','"+userid+"','Editor','"+time+"');")
        flash("You just created the '"+groupname+"' MyBook Group" , "success")


    
    return render_template('mygroups.html',editprofile=EditProfile(),searchform=SearchForm(), uploadform=uploadform, createGroupForm=createGroupForm, groups=groups,profilepic=session['profilepic'],fname=session['fname'],username= session['username'],lname=session['lname'],email=session['email'],location=session['location'],biography=session['biography'],followers=session['followers'],following=session['following'],userid=session['userid'])


@app.route('/creategrouppost/<groupID>/<postType>', methods=['POST', 'GET'])
def creategrouppost(groupID, postType):
    createpost = CreatePost()
    textpost=createpost.text.data
    
    if request.method == "POST":
        #SELECT userid FROM joinsgroup WHERE status = 'Editor' AND userid = 42 AND groupid = 1;
        value=db.engine.execute("SELECT userid FROM joinsgroup WHERE status = 'Editor' AND userid = '"+session['userid']+"' AND groupid = '"+groupID+"';")
        
        isEditor = 0
        for val in value:
            isEditor = val

        if isEditor:
            if postType == 'text' and textpost!="":
                db.engine.execute("insert into  posts(content,ctype, postDateTime) values('"+textpost+"','text','"+str(datetime.datetime.now())+"')")
                lastTextPostID= db.engine.execute("SELECT postid FROM posts ORDER BY postid DESC LIMIT 1")
                for last in lastTextPostID:
                    postid=last.postid
                db.engine.execute("INSERT INTO  groupposts(groupid,postid) values('"+groupID+"', '"+str(postid)+"');")
                # db.engine.execute("insert into user_post_log(postid ,userid) values ('"+str(postid)+"','"+session['userid']+"')")
                cur.execute("CALL adduserposts("+str(postid)+",'"+str(session['userid'])+"')")
                conn.commit()
                return groupposts(groupID)

            elif postType == 'image':
                photo= createpost.image.data
                filename=secure_filename(photo.filename)
                photo.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                db.engine.execute("insert into gallery(photourl) values('"+'/static/uploads/'+filename+"')")
                lastphotoid= db.engine.execute("select photoid from gallery order by photoid desc limit 1")
                for last in lastphotoid:
                    photoid=last.photoid
                # db.engine.execute("insert into addphoto(photoid ,userid) values ('"+str(photoid)+"','"+session['userid']+"')")
                cur.execute("CALL addphotos("+str(photoid)+",'"+str(session['userid'])+"')")
                conn.commit()
                db.engine.execute("insert into  posts(content,ctype, postDateTime) values('"+'/static/uploads/'+filename+"','image','"+str(datetime.datetime.now())+"')")

                lastpostid= db.engine.execute("select postId from posts order by postid desc limit 1")
                for last in lastpostid:
                    postId=last.postid

                # db.engine.execute("insert into user_post_log(postid ,userid) values ('"+str(postId)+"','"+session['userid']+"')")
                cur.execute("CALL adduserposts("+str(postId)+",'"+str(session['userid'])+"')")
                conn.commit()
                db.engine.execute("INSERT INTO  groupposts(groupid,postid) values('"+groupID+"', '"+str(postId)+"');")

                return groupposts(groupID)

        else:
            flash('You are not a Content Editor for this group!', 'danger')
            return groupposts(groupID)
        


@app.route('/groupposts/<groupid>')
def groupposts(groupid):
    commentform=Comment()
    uploadform=UploadProfilePic()
    form=CreatePost()
    grouppostinfo=[]
    groupinfo=db.engine.execute("SELECT * FROM groups join profiles on profiles.userid=groups.createdby WHERE groupid = '"+groupid+"'")
    groupmembers = db.engine.execute("SELECT * FROM joinsgroup JOIN users ON users.userid = joinsgroup.userid INNER JOIN profiles ON profiles.userid = users.userid JOIN gallery ON gallery.photoid = profiles.profilepic WHERE groupid = '"+groupid+"'")
    nonMembers = db.engine.execute("SELECT * FROM users u JOIN profiles p ON u.userid = p.userid INNER JOIN gallery g ON g.photoid = p.profilepic WHERE u.userid NOT IN (SELECT userid FROM joinsgroup WHERE groupid = "+groupid+") order by u.userid desc limit 20")
    ingroup=False
    for x in groupmembers:
        if(int(session['userid'])==x.userid):
            ingroup=True

    if(ingroup):
        groupposts=db.engine.execute("select user_post_log.postid, user_post_log.userid, content, ctype, postdatetime, profileno, profilepic, username, countryliving, photoid, photourl from user_post_log join (SELECT * FROM posts WHERE postid IN (SELECT postid FROM groupposts WHERE groupid = "+groupid+")) AS posts on posts.postid=user_post_log.postid INNER join profiles on profiles.userid=user_post_log.userid  INNER join gallery on profiles.profilepic=gallery.photoid order by posts.postid desc")
    else:
        groupposts=[]
    for a in groupinfo:
        creatorid = a.createdby
        groupname = a.groupname
        createddate = a.createddate
        groupcreator = a.username


    return render_template('groupPosts.html',editprofile=EditProfile(), form=form, uploadform=uploadform, searchform=SearchForm(),  creatorid=int(creatorid), groupid = groupid, groupname=groupname, groupmembers=groupmembers,nonMembers=nonMembers, createddate=createddate, commentform=commentform, creator=groupcreator, groupinfo=groupinfo, posts=groupposts,profilepic=session['profilepic'],fname=session['fname'],username= session['username'],lname=session['lname'],email=session['email'],location=session['location'],biography=session['biography'],followers=session['followers'],following=session['following'],userid=int(session['userid']))
 
@app.route('/groupstatus/<groupid>/<userid>/<status>',methods=['POST', 'GET'])
def groupstatus(groupid, userid, status):
    if request.method == "POST":
        if str(status) == 'Editor':
            db.engine.execute("UPDATE joinsgroup SET status =  'Viewer' WHERE groupid = "+groupid+" AND userid = "+userid)
        else:
            db.engine.execute("UPDATE joinsgroup SET status =  'Editor' WHERE groupid = "+groupid+" AND userid = "+userid)
    return groupposts(groupid)

@app.route('/joingroup/<groupID>/<userID>')
def joingroup(groupID, userID):
    value=db.engine.execute("SELECT userid FROM joinsgroup WHERE userid = '"+userID+"' AND groupid = '"+groupID+"'")
    exists = 0
    for val in value:
        exists = val
    
    if exists:
        flash("You are already a member of this group!", "danger")
        groups=db.engine.execute("SELECT * FROM groups")
        return groupposts(groupID)
    else:
        time = datetime.datetime.now()
        time = time.strftime("%Y-%m-%d %H:%M:%S")
        db.engine.execute("INSERT INTO joinsGroup (groupid,userid,status,joindate) values('"+groupID+"','"+userID+"','Viewer','"+time+"')")
        flash("You are now a member of this group!", "success")
        return groupposts(groupID)
        
@app.route('/addmember/<groupid>/<userid>', methods=['POST', 'GET'])
def addmember(groupid, userid):
    if request.method == "POST":
        time = datetime.datetime.now()
        time = time.strftime("%Y-%m-%d %H:%M:%S")
        db.engine.execute("INSERT INTO joinsGroup (groupid,userid,status,joindate) values('"+groupid+"','"+userid+"','Editor','"+time+"')")
        flash("You just added a new member to this group!", "success")
        return redirect(url_for('groupposts', groupid=groupid))
    return

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
                db.engine.execute("insert into Users (firstname,lastname,email,gender,password) values('"+fname+"','"+lname+"','"+email+"','"+gender+"','"+password+"')")
                

                return redirect(url_for('setupprofile'))
    else:
                flash_errors(createuser)
    return render_template('signup.html',form=createuser)  

@app.route('/friendlist/<userid>',)
def friendlist(userid):
    friends=db.engine.execute("select * from friendship join users on users.userid=friendship.fuserid join profiles on profiles.userid=users.userid join gallery on gallery.photoid=profiles.profilepic where friendship.userid='"+userid+"' ")
    work=db.engine.execute("select * from friendship join users on users.userid=friendship.fuserid join profiles on profiles.userid=users.userid join gallery on gallery.photoid=profiles.profilepic where ftype='Work' AND friendship.userid='"+userid+"' ")
    school=db.engine.execute("select * from friendship join users on users.userid=friendship.fuserid join profiles on profiles.userid=users.userid join gallery on gallery.photoid=profiles.profilepic where ftype='School' AND friendship.userid='"+userid+"' ")
    relatives=db.engine.execute("select * from friendship join users on users.userid=friendship.fuserid join profiles on profiles.userid=users.userid join gallery on gallery.photoid=profiles.profilepic where ftype='Relatives' AND friendship.userid='"+userid+"' ")
    # need to choice which one is more optimized
    # select * from friendship join users on users.userid=friendship.fuserid join profiles on profiles.userid=users.userid where friendship.userid=2;

    # select * from users join ((select fuserid,ftype from friendship where userid=2) as friends join (select userid,profileno,profilepic,username,biography,countryliving from profiles)as profile on profile.userid=friends.fuserid) as friend on friend.fuserid=users.userid;
    uploadform=UploadProfilePic()

    return render_template('friendslist.html',editprofile=EditProfile(), searchform=SearchForm(), uploadform=uploadform,work=work, school=school, relatives=relatives, friends=friends,profilepic=session['profilepic'],fname=session['fname'],username= session['username'],lname=session['lname'],email=session['email'],location=session['location'],biography=session['biography'],followers=session['followers'],following=session['following'],userid=session['userid'])


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
                lastuserid= db.engine.execute("select userid from users order by userid desc limit 1")
                for last in lastuserid:
                    userid=last.userid
                # insert into gallery and addphoto , get the id from that for profilepic
                db.engine.execute("insert into gallery(photourl) values('"+'/static/uploads/'+filename+"')")
                lastphotoid= db.engine.execute("select photoid from gallery order by photoid desc limit 1")
                for last in lastphotoid:
                    photoid=last.photoid
              
                # db.engine.execute("insert into addphoto(photoid ,userid) values ('"+str(photoid)+"','"+str(userid)+"')")
                cur.execute("CALL addphotos("+str(photoid)+",'"+str(userid)+"')")
                conn.commit()
                db.engine.execute("insert into Profiles (userid,profilepic,username,biography,countryliving,createddate) values('"+str(userid)+"','"+str(photoid)+"','"+username+"','"+biography+"','"+location+"','"+format_date_joined(datetime.datetime.now())+"')")
		

                return redirect(url_for('login'))
    else:
                flash_errors(createprofile)
    return render_template('setupprofile.html',form=createprofile)   

@app.route('/addfollower/<followerid>',methods=['POST'])
def addfollower(followerid):
    form=FriendType()
    friendtype = form.friendtype.data
    # print(friendtype)
    session['following']+=1
    session['followers']+=1

    cur.execute("CALL addfriend("+str(session['userid'])+","+str(followerid)+",'"+friendtype+"')")
    conn.commit()
    cur.execute("CALL addfriend("+str(followerid)+","+str(session['userid'])+",'"+friendtype+"')")
    conn.commit()
    return redirect(url_for('profile',userid=followerid))

@app.route('/deletefollower/<followerid>',methods=['POST',"Get"])
def deletefollower(followerid):
    form=FriendType()
    friendtype = form.friendtype.data
    # print(friendtype)
    session['following']-=1
    session['followers']-=1
    db.engine.execute("delete from  Friendship where userid="+str(session['userid'])+" and fuserid="+str(followerid))
    db.engine.execute("delete from  Friendship where userid="+str(followerid)+" and fuserid="+str(session['userid']))

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
            # db.engine.execute("insert into addphoto(photoid ,userid) values ('"+str(photoid)+"','"+session['userid']+"')")
            cur.execute("CALL addphotos("+str(photoid)+",'"+str(session['userid'])+"')")
            conn.commit()
            db.engine.execute("insert into  posts(content,ctype, postDateTime) values('"+'/static/uploads/'+filename+"','image','"+str(datetime.datetime.now())+"')")

        lastpostid= db.engine.execute("select postId from posts order by postid desc limit 1")
        for last in lastpostid:
            postId=last.postid
        # db.engine.execute("insert into user_post_log(postid ,userid) values ('"+str(postId)+"','"+session['userid']+"')")
        cur.execute("CALL adduserposts("+str(postId)+",'"+str(session['userid'])+"')")
        conn.commit()
        return redirect(url_for('posts'))
   
    
@app.route('/setprofilepic/<photoid>')
def setprofilepic(photoid):
    setprofilepic=db.engine.execute("update profiles set profilepic='"+str(photoid)+"' where userid="+session['userid'])
    print(photoid)
  
    getprofilepic=db.engine.execute("select photourl from gallery where photoid="+str(photoid))
    for m in getprofilepic:
        session['profilepic']=m.photourl

    return redirect(url_for('myprofile'))

@app.route('/uploadgallery',methods=['POST'])
def uploadgallery():
    uploadform=UploadProfilePic()
     # insert into gallery and addphoto , get the id from that for profilepic

    photo= uploadform.profilepic.data
    created_date=format_date_joined(datetime.datetime.now())
    filename=secure_filename(photo.filename)
    photo.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
    db.engine.execute("insert into gallery(photourl) values('"+'/static/uploads/'+filename+"')")
    lastphotoid= db.engine.execute("select photoid from gallery order by photoid desc limit 1")
    for last in lastphotoid:
        photoid=last.photoid
    
    # db.engine.execute("insert into addphoto(photoid ,userid) values ('"+str(photoid)+"','"+str(session['userid'])+"')")
    cur.execute("CALL addphotos("+str(photoid)+",'"+str(session['userid'])+"')")
    conn.commit()
    return redirect(url_for('setprofilepic',photoid=photoid))

@app.route('/profile/<userid>')
def profile(userid):
    friendship=False
    form=FriendType()
    commentform=Comment()
    uploadform=UploadProfilePic()
    users=db.engine.execute("select * from profiles join users on profiles.userid=users.userid join gallery on gallery.photoid=profiles.profilepic where users.userid='"+userid+"'")
    # posts=db.engine.execute("select * from (select * from texts union select * from  images)as allpost join posts on posts.postid= allpost.postid join profiles on posts.userid=profiles.userid  where posts.userid='"+str(userid)+"' order by posts.postid desc")
    # checking if loggedin user  is friends with the userid
    friends=db.engine.execute("select * from friendship where userid="+str(session['userid'])+"and fuserid="+str(userid))
    for x in friends:
        friendship=True

    if(friendship):
        posts=db.engine.execute("select * from user_post_log join posts on posts.postid=user_post_log.postid  join profiles on profiles.userid=user_post_log.userid  join gallery on profiles.profilepic=gallery.photoid where profiles.userid='"+str(userid)+"' order by posts.postid desc")
    else:
        posts=[]
    postsCounts= db.engine.execute("SELECT COUNT(postid) AS post_counts FROM user_post_log  where userid="+userid+" and postid NOT IN(select postid from groupposts)")
    for x in postsCounts:
        postcount=x.post_counts
    friends=db.engine.execute("select count(userid) as following from friendship where fuserid='"+userid+"'")  
    for x in friends:
                # print(x.following)
        userfollower=x.following
    return render_template('profilepage.html',userfollower=userfollower,postcount=postcount,editprofile=EditProfile(),searchform=SearchForm(), uploadform=uploadform,commentform=commentform,fform=form,posts=posts,users=users,profilepic=session['profilepic'],fname=session['fname'],username= session['username'],lname=session['lname'],email=session['email'],location=session['location'],biography=session['biography'],followers=session['followers'],following=session['following'],userid=session['userid'])

@app.route('/editprofile',methods=['POST','GET'])
def editprofile():
    editprofile=EditProfile()
    if request.method == "POST":
        username=editprofile.username.data
        if(username!=session['username']):
            db.engine.execute("update profiles set username='"+username+"' where userid="+session['userid'])
            session['username']=username

        lname=editprofile.lname.data
        if(lname!=session['lname']):
            db.engine.execute("update users set lastname='"+lname+"' where userid="+session['userid'])
            session['lname']=lname


        fname=editprofile.fname.data
        if(fname!=session['fname']):
            db.engine.execute("update users set firstname='"+fname+"' where userid="+session['userid'])
            session['fname']=fname


        email=editprofile.email.data
        if(email!=session['email']):
            db.engine.execute("update users set email='"+email+"' where userid="+session['userid'])
            session['email']=email


    
        # gender = editprofile.gender.data
        # if(email!=session['gender']):
        #     db.engine.execute("update")

        
        password =editprofile.password.data
        repassword = editprofile.repassword.data

        if(password!="" and repassword!="" and password==repassword):
            db.engine.execute("update users set password='"+password+"' where userid="+session['userid'])

        
        location = editprofile.location.data
        if(location!=session['location']):
            db.engine.execute("update profiles set countryliving='"+location+"' where userid="+session['userid'])
            session['location']=location


        # biography = editprofile.biography.data
        # if(biography!=""):
        #     db.engine.execute("update profiles set biography='"+biography+"'")

     

        return redirect(url_for('posts'))
    return render_template('editprofile.html',editprofile=editprofile,searchform=SearchForm(),profilepic=session['profilepic'],fname=session['fname'],username= session['username'],lname=session['lname'],email=session['email'],location=session['location'],biography=session['biography'],followers=session['followers'],following=session['following'],userid=session['userid'])
@app.route('/myprofile')
def myprofile():
    form=CreatePost()

    fform=FriendType()
    commentform=Comment()
    uploadform=UploadProfilePic()
    users=db.engine.execute("select * from profiles join users on profiles.userid=users.userid join gallery on gallery.photoid=profiles.profilepic where users.userid='"+session['userid']+"'")
    # posts=db.engine.execute("select * from (select * from texts union select * from  images)as allpost join posts on posts.postid= allpost.postid join profiles on posts.userid=profiles.userid  where posts.userid='"+str(userid)+"' order by posts.postid desc")
    posts=db.engine.execute("select * from user_post_log join posts on posts.postid=user_post_log.postid  join profiles on profiles.userid=user_post_log.userid  join gallery on profiles.profilepic=gallery.photoid where profiles.userid='"+str(session['userid'])+"' AND user_post_log.postid NOT IN(SELECT postid FROM groupposts) order by posts.postid desc")
    postsCounts= db.engine.execute("SELECT COUNT(postid) AS post_counts FROM user_post_log  where userid="+session['userid']+" and postid NOT IN(select postid from groupposts)")
    for x in postsCounts:
        postcount=x.post_counts

    return render_template('myprofilepage.html',postcount=postcount,editprofile=EditProfile(),searchform=SearchForm(), form=form,uploadform=uploadform,commentform=commentform,fform=fform,posts=posts,users=users,profilepic=session['profilepic'],fname=session['fname'],username= session['username'],lname=session['lname'],email=session['email'],location=session['location'],biography=session['biography'],followers=session['followers'],following=session['following'],userid=session['userid'])


# all individual posts for a specific user
@app.route('/posts/<userid>')
def userposts(userid):
    form=CreatePost()
    fform=FriendType()

    commentform=Comment()
    users=db.engine.execute("select * from profiles join users on profiles.userid=users.userid where users.userid='"+userid+"'")
    # posts=db.engine.execute("select * from (select * from texts union select * from  images)as allpost join posts on posts.postid= allpost.postid join profiles on posts.userid=profiles.userid  where posts.userid='"+str(userid)+"' order by posts.postid desc")
    posts=db.engine.execute("select * from user_post_log join posts on posts.postid=user_post_log.postid where posts.userid='"+str(userid)+"' order by posts.postid desc")
   
    return render_template('profilepage.html',editprofile=EditProfile(),searchform=SearchForm(), fform=fform,commentform=commentform,posts=posts,form=form,users=users,profilepic=session['profilepic'],fname=session['fname'],username= session['username'],lname=session['lname'],email=session['email'],location=session['location'],biography=session['biography'],followers=session['followers'],following=session['following'],userid=session['userid'])

    # return render_template('posts.html',form=form,posts=posts,comments=comments,profilepic=session['profilepic'],fname=session['fname'],username= session['username'],lname=session['lname'],email=session['email'],location=session['location'],biography=session['biography'],followers=session['followers'],following=session['following'],userid=session['userid'])

@app.route('/addcomment/<postid>',methods=['GET','POST'])
def addcomment(postid):
    print("adding comment")
    form=Comment()
    commentDetail=form.comment.data
  
    addcomments=db.engine.execute("insert into comments(commentdetail,commentdatetime) values('"+commentDetail+"','"+str(datetime.datetime.now())+"')")
    lastcommentid=db.engine.execute("select commentid from comments order by commentid desc limit 1")
    for x in lastcommentid:
        commentid=x.commentid
    db.engine.execute("insert into addcomments(commentid,postid,userid) values('"+str(commentid)+"','"+str(postid)+"','"+str(session['userid'])+"')")

    return redirect(url_for('posts',userid=session['userid']))

@app.route('/comments/<postid>')
def comments(postid):
    # comments=db.engine.execute("select * from comments where postid='"+str(postid)+"'")
    return render_template('comments.html',comments=comments)


@app.route('/searchuser',methods=['POST'])
def searchuser():
    form=CreatePost()
    fform=FriendType()
    uploadform=UploadProfilePic()
    searcform=SearchForm()
    commentform=Comment()
    searchusername=searcform.username.data
    searchusers=db.engine.execute(" select username,photourl,firstname,lastname,countryliving,profile.userid from (SELECT username,countryliving,userid,profilepic FROM profiles WHERE lower(username) LIKE '"+searchusername.lower()+"%%') as profile inner join users on profile.userid=users.userid inner join gallery on gallery.photoid=profile.profilepic limit 10")
    return render_template('searchlist.html',editprofile=EditProfile(),uploadform=uploadform,searchusers=searchusers,searchform=SearchForm(), fform=fform,commentform=commentform,posts=posts,form=form,profilepic=session['profilepic'],fname=session['fname'],username= session['username'],lname=session['lname'],email=session['email'],location=session['location'],biography=session['biography'],followers=session['followers'],following=session['following'],userid=session['userid'])


@app.route('/adminsearchuser',methods=['POST'])
def adminsearchuser():
    searcform=SearchForm()
    searchusername=searcform.username.data
    searchusers=db.engine.execute(" select username,photourl,firstname,lastname,countryliving,profile.userid from (SELECT username,countryliving,userid,profilepic FROM profiles WHERE lower(username) LIKE '"+searchusername.lower()+"%%') as profile inner join users on profile.userid=users.userid inner join gallery on gallery.photoid=profile.profilepic limit 10")

    return render_template('adminsearchlist.html',allusers=searchusers,searchform=SearchForm())

@app.route('/page/<id>')
def page(id):
    searcform=SearchForm()
    userprofile=db.engine.execute("select * from profiles join users on profiles.userid=users.userid join gallery on gallery.photoid=profiles.profilepic where users.userid='"+id+"'")
    userposts=db.engine.execute("select * from user_post_log join posts on posts.postid=user_post_log.postid join profiles on profiles.userid=user_post_log.userid join gallery on profiles.profilepic=gallery.photoid where user_post_log.userid='"+id+"' order by posts.postid desc")
    return render_template('page.html',userprofiles=userprofile,userposts=userposts,searchform=SearchForm())


@app.route('/')
@app.route('/login', methods=['POST', 'GET'])
def login():
    loginform=Login()
    if request.method == "POST" and  loginform.validate_on_submit():
        username=loginform.username.data
        password=loginform.password.data
        if username=="admin" and password=="1234":
            return redirect(url_for('userinfo'))
        profile=db.engine.execute("select * from profiles join users on profiles.userid=users.userid where profiles.username='"+username+"' and password='"+password+"' limit 1")  
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

@app.route('/userinfo' ,methods=['GET', 'POST'])
def userinfo():

    userCount= db.engine.execute("SELECT COUNT(userid) AS users_count FROM users")
    totalUsers = 0
    for val in userCount:
        totalUsers = val.users_count

    avgGroupCreated=db.engine.execute("SELECT AVG(create_count) AS avg_create FROM (SELECT COUNT(groupid) AS create_count FROM groups GROUP BY createdby) AS avg_Create")
    averageGroupsCreatedPerUser = 0
    for val in avgGroupCreated:
        averageGroupsCreatedPerUser = val.avg_create

    avgGroupJoined=db.engine.execute("SELECT AVG(join_Count) AS avg_joined FROM (SELECT COUNT(groupid) AS join_Count FROM joinsgroup GROUP BY userid) AS avg_Joined")
    averageGroupsJoinedPerUser = 0
    for val in avgGroupJoined:
        averageGroupsJoinedPerUser = val.avg_joined


    userInfoList = []

    friendsCount = db.engine.execute("SELECT userid, COUNT(fuserid) AS friends_count FROM friendship GROUP BY (userid) ORDER BY (userid) desc")
    
    for user in friendsCount:

        usernames = db.engine.execute("SELECT username FROM profiles where userid="+str(user.userid))

        for username in usernames:
            currentUserName = username.username
        
        currentUserInfo = [currentUserName, 0, 0, 0]
        currentUserInfo[1] = user.friends_count

        postsCount= db.engine.execute("SELECT COUNT(postid) AS post_counts FROM user_post_log where userid="+str(user.userid))
        for noOfPosts in postsCount:
            currentUserInfo[2] = noOfPosts.post_counts
        
        commentsCount=db.engine.execute("SELECT COUNT(commentid) AS comment_counts FROM addcomments where userid="+str(user.userid))
        for noOfComments in commentsCount:
            currentUserInfo[3] = noOfComments.comment_counts
                
        
        userInfoList.append(currentUserInfo)

    return render_template('userInfo.html', userInfoList=userInfoList, totalUsers=totalUsers, averageGroupsCreatedPerUser=int(round(averageGroupsCreatedPerUser)), averageGroupsJoinedPerUser=int(round(averageGroupsJoinedPerUser)), searchform = SearchForm())

@app.route('/groupinfo' ,methods=['GET', 'POST'])
def groupinfo():

    groupCount= db.engine.execute("SELECT COUNT(groupid) AS noofgroups FROM groups ")
    totalGroups = 0
    for val in groupCount:
        totalGroups = val.noofgroups

    avgPostsCount=db.engine.execute("SELECT AVG(post_count) AS avg_posts FROM (SELECT COUNT(postid) AS post_count FROM groupposts GROUP BY groupid) AS avg_Posts")
    averagePostsPerGroup = 0
    for val in avgPostsCount:
        averagePostsPerGroup = val.avg_posts

    average_members= db.engine.execute("SELECT AVG(no_members) AS avg_members FROM (SELECT COUNT(userid) AS no_members FROM joinsgroup GROUP BY groupid) AS avgMembers;")
    avgMembers = 0
    for val in average_members:
        avgMembers = val.avg_members


    groupInfoList = []

    groupIDs= db.engine.execute("SELECT groupid FROM groups ORDER BY(groupid)")

    for groupID in groupIDs:
        for val in groupID:
            currentGroupID = str(val)

        groupnames= db.engine.execute("SELECT groupname FROM groups WHERE groupid = "+currentGroupID)
        for text in groupnames:
            groupname = text.groupname
        
        noofmembers = db.engine.execute("SELECT COUNT(userid) AS members FROM joinsgroup WHERE groupid = "+currentGroupID+" GROUP BY(groupid)")
        for val in noofmembers:
            members = val.members

        noofposts = db.engine.execute("SELECT count(postid) AS posts FROM groupposts WHERE groupid = "+currentGroupID+" GROUP BY(groupid)")
        for val in noofposts:
            posts = val.posts

        groupcreators = db.engine.execute("SELECT username FROM groups g JOIN profiles p ON CAST(g.createdby AS INTEGER) = p.userid WHERE groupid = "+currentGroupID+"")
        for text in groupcreators:
            groupcreator = text.username

        currentGroupInfo = [groupname, members, posts, groupcreator]
        groupInfoList.append(currentGroupInfo)
        

    return render_template('groupInfo.html', groupInfoList=groupInfoList, totalGroups=totalGroups, avgMembers=int(round(avgMembers)), averagePostsPerGroup=int(round(averagePostsPerGroup)), searchform = SearchForm())

@app.route('/postinfo' ,methods=['GET', 'POST'])
def postinfo():

    postsCount=db.engine.execute("SELECT COUNT(postid) AS noofposts FROM posts")
    totalPosts = 0
    for val in postsCount:
        totalPosts = val.noofposts

    avgPosts=db.engine.execute("SELECT AVG(noOfposts) AS avgposts FROM (SELECT COUNT(postid) AS noOfposts FROM user_post_log GROUP BY(userid)) AS postsPerUser")
    averageNumberOfPosts = 0
    for val in avgPosts:
        averageNumberOfPosts = val.avgposts

    avgLikes = db.engine.execute("SELECT AVG(likes) AS avglikes FROM (SELECT COUNT(userid) AS likes FROM likes GROUP BY(postid)) AS noOfLikes")
    averageNumberOfLikes = 0
    for val in avgLikes:
        averageNumberOfLikes = val.avglikes
    

    postInfoList = []

    postIDs=db.engine.execute("SELECT postid FROM posts order by postid desc limit 100")

    for postID in postIDs:
        for val in postID:
            currentPostID = str(val)

        currentpostType = db.engine.execute("SELECT ctype FROM posts WHERE postid = "+currentPostID)
        for text in currentpostType:
            postType = text.ctype
        
        noOfLikes = db.engine.execute("SELECT COUNT(userid) as likes FROM likes WHERE postid ="+currentPostID)
        for val in noOfLikes:
            likes = val.likes

        postOwner = db.engine.execute("SELECT username FROM user_post_log upl JOIN profiles p ON upl.userid = p.userid WHERE postid ="+currentPostID)
        for text in postOwner:
            owner = text.username

        currentPostInfo = [currentPostID, postType, likes, owner]

        postInfoList.append(currentPostInfo)


    return render_template('postInfo.html', postInfoList=postInfoList, searchform = SearchForm(), totalPosts=totalPosts, averageNumberOfPosts=int(round(averageNumberOfPosts)), averageNumberOfLikes=int(round(averageNumberOfLikes)))


@app.route('/logout')
def logout():
    flash("Logged out successfully!!!","success")
    loginform=Login()
    return redirect('login')

@app.route('/allusers')
def allusers():
    allusers=db.engine.execute("select * from users join profiles on profiles.userid=users.userid join gallery on gallery.photoid=profiles.profilepic ORDER BY(profileno) desc limit 3000")

    return render_template('allusers.html', allusers=allusers, searchform = SearchForm())

@app.route('/allgroups')
def allgroups():
    allgroups=db.engine.execute("SELECT * FROM groups g JOIN profiles p ON CAST(g.createdby AS INTEGER) = p.userid ORDER BY(groupid)")
    return render_template('allgroups.html', allgroups=allgroups, searchform = SearchForm())

@app.route('/allposts')
def allposts():
    allposts=db.engine.execute("select * from user_post_log join posts on posts.postid=user_post_log.postid join profiles on profiles.userid=user_post_log.userid join gallery on profiles.profilepic=gallery.photoid order by posts.postid desc limit 300")
    return render_template('allposts.html', allposts=allposts, searchform = SearchForm())

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
    return render_template('404.html',searchform=SearchForm()), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
