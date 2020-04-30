from faker import Faker
import random
import functools
fake=Faker()

# userid starts with US 
# commentid starts with CM
# postid starts with PS
# groupid starts with GP
# textid starts with TT
# imageid starts with IM
# profileno starts with PF


f= open("database.sql","w+")
#creation of each user and profiles

# db.engine.execute("create table Users(userid SERIAL unique,firstName varchar(255),lastName varchar(255),email varchar(50),gender varchar(64),password text,primary key(userId))")
# db.engine.execute("create table Profiles(profileNo SERIAL unique,userid int unique,profilePic int,username text,biography text,countryLiving varchar(30),primary key (userId,profileNo),foreign key(userId) references Users(userId) on delete cascade on update cascade)")

for i in range(100):
    userid = i+1
    profileNo=userid
    if(random.randint(0,20)%2==0):
        fakename=fake.name_female().split(" ")
        gender="female"
    else:
        fakename=fake.name_male().split(" ")
        gender="male"
    address=fake.address().split("\n")
    address1=address[0]
    address2=address[1].split(",")
    country=address2[0]

    digit= functools.partial(random.randint, 0, 9)
    fakephonenum = lambda: "+{}-{}{}{}-{}{}{}-{}{}{}{}".format(digit(), digit(), digit(), digit(), digit(), digit(), digit(), digit(), digit(), digit(), digit())
    phonenumber=fakephonenum()
    firstname=fakename[0]
    lastname=fakename[1]
    username=firstname[:3]+lastname[-3:]+str(i)
    email=fake.free_email()

    # profilepic=fake.image_url()
    password=fake.password(length=40, special_chars=False, upper_case=True)
    # encodedpassword=password.encode('utf-16')
    # decodedtext=encodedtext.decode('utf-16')
    # print(decodedtext)
    # while("placeimg" not in profilepic):
    #     profilepic=fake.image_url()
    profilepic=random.randint(1,500)
    biography=fake.text()
    
    # appending to text file
    biography.replace('\r','')
    f.write("insert into Users (firstname,lastname,email,gender,password) values('"+firstname+"','"+lastname+"','"+email+"','"+gender+"','"+str(password)+"'); \n")

    f.write("insert into Profiles (userid,profilepic,username,biography,countryliving) values('"+str(userid)+"','"+str(profilepic)+"','"+username+"','"+biography+"','"+country+"');\n")

   
    print(str(i)+"\n")
print(" creation of users and profiles done")


# db.engine.execute("create table gallery(photoid SERIAL,photourl text,primary key (photoid) )")
# db.engine.execute("create table addphoto(photoid int unique,userid int unique,primary key (photoid,userid), foreign key (userid) references Users(userid) on delete cascade on update cascade,foreign key (photoid) references gallery(photoid) on delete cascade on update cascade  )")

for x in range(1000):
    photoid=x+1
    photourl=fake.image_url()
    while("placeimg" not in photourl):
        photourl=fake.image_url()
    userid=random.randint(1,100)
    f.write("insert into gallery (photourl) values('"+photourl+"'); \n")
    f.write("insert into addphoto (photoid,userid) values('"+str(photoid)+"','"+str(userid)+"'); \n")

# db.engine.execute("create table posts(postId SERIAL unique, content text, ctype varchar(15), postDate_Time timestamp,primary key (postId))")

# db.engine.execute("create table user_post_log(postId int, userid int,primary key (userId,postId),foreign key(userId) references Users(userId) on delete cascade on update cascade)")


textId=1
imageId=1
commentId=1
#creation of 3000000 posts 
for x in range(100):

    #selecting the userid for the post 
    postId=x+1
    userId=random.randint(1,50)
    postdatetime=fake.date_time_this_year()
    #even for text - odd for post
    text_photo=random.randint(0,20)
    if(text_photo%2==0):
        content= fake.paragraph()
        ctype="text"
        textId+=1

    else:
        content=fake.image_url()
        while("placeimg" not in content):
            content=fake.image_url()
        ctype="image"

        imageId+=1

    f.write("insert into posts (content,ctype,postdatetime) values('"+str(content)+"','"+str(ctype)+"','"+str(postdatetime)+"');\n")
    f.write("insert into user_post_log (postId,userid ) values('"+str(postId)+"','"+str(userId)+"');\n")

        #insert into image
    #creation of at least 2-40 comments on post
    randnum=random.randint(2,10)
    for y in range(randnum):
        # userid of comment
        cuserid=random.randint(1,50)
        while(userid==cuserid):
            cuserid=random.randint(1,50)
        commentDetail=fake.text(max_nb_chars=150, ext_word_list=None)
        commentDetail.replace('\r','')
        commentDateTime=fake.date_time_this_decade()
        # insert into comments 
        




# db.engine.execute("create table comments(commentId SERIAL,commentDetail varchar(255),commentDateTime timestamp,primary key (commentId) )")

# db.engine.execute("create table addcomments(commentId int,postId int,primary key(commentId,postId))")

        f.write("insert into comments (commentDetail,commentDateTime) values('"+commentDetail+"','"+str(commentDateTime)+"');\n")
        f.write("insert into addcomments (commentId ,postId,userid ) values('"+str(commentId)+"','"+str(postId)+"','"+str(cuserid)+"');\n");

        commentId+=1
        #likes
        # for z in 

    randum=random.randint(2,50)
    for m in range(randum):
        f.write("insert into likes (postid,userid) values('"+str(postId)+"','"+str(m+1)+"');\n")


print(" creation of post,likes,comments done")




# db.engine.execute("create table Friendship(userid int,fuserid int,fType varchar(255),primary key(userId,fUserId),foreign key (userId) references Users(userId) on delete cascade on update cascade,foreign key (fuserId) references Users(userId) on delete cascade on update cascade)")


# friends 
allfriendship=[]
for x in range(50):
    # creation of friends
    userid=x+1
    friends=[]
    relationships=["Relatives", "School", "Work"]

    randnum=random.randint(1,20)
    for y in range(randnum):
        friendid=random.randint(1,50)
        # while((friendid in friends)):
        #     friendid=random.randint(1,50)
        # while((friendid==userid)):
        #     friendid=random.randint(1,50)
        fType=random.choice(relationships)

        friends.append(friendid)
        # allfriendship.append((friendid,userid))
        if(friendid==userid):
            print("cant be friend with self")
            continue
        elif(([userid,friendid] not in allfriendship) and ([friendid,userid] not in allfriendship)):

            f.write("insert into Friendship (userid,fuserid,ftype) values('"+str(userid)+"','"+str(friendid)+"','"+fType+"');\n")
            f.write("insert into Friendship (userid,fuserid,ftype) values('"+str(friendid)+"','"+str(userid)+"','"+fType+"');\n")
            allfriendship.append([userid,friendid])
            print('newfriends')
        else:
            print('friendsalready')
    


    print(x)
for p in allfriendship:
    print(p)
print(" creation of friendships done")

# db.engine.execute("create table groups(groupId SERIAL,groupName varchar(255),createdBy varchar(255),primary key(groupId))")

# db.engine.execute("create table joinsGroup(groupId int,userid int,status varchar(255),primary key(groupId,userId),foreign key(groupId) references groups(groupId) on delete cascade on update cascade,foreign key(userId) references Users(userId) on delete cascade on update cascade)")

#create groups
users=[]
status_all=["Editor","Viewer"]
for x in range(20):
    breaking=False
    groupId=x+1
    groupName1=fake.word()
    groupName2=fake.word()
    groupName=groupName1+" "+groupName2
    createdBy= random.randint(1,50)
    createddate=fake.date_time_this_year()
    f.write("insert into groups (groupname,createdby,createddate) values('"+groupName+"','"+str(createdBy)+"','"+str(createddate)+"');\n")

    randnum=random.randint(2,5)
    for y in range(randnum):
        potentialusers=list(range(1, 50))

        userId=random.choice(potentialusers)
        
        while((createdBy==userId) or (userId in users)):
            if(potentialusers==[]):
                breaking=True
                break
            else:
                userId=random.choice(potentialusers)
                potentialusers= [x for x in potentialusers if x != userId]
        if(breaking==False):
            users.append(userId)
            status=random.choice(status_all)
            joindate=fake.date_time_this_year()
            f.write("insert into joinsGroup (groupid,userid,status,joindate) values('"+str(groupId)+"','"+str(userId)+"','"+status+"','"+str(joindate)+"');\n")
    print(x+1)

print(" creation of groups done")


# db.engine.execute("create table groupPosts(groupId int,postid int,primary key(groupId,postid),foreign key(groupId) references groups(groupId) on delete cascade on update cascade,foreign key(postId) references posts(postId) on delete cascade on update cascade)")
for x in range(20):
        # groupid=random.randint(1,20)
        randnum=random.randint(5,20)
        for y in range(randnum):
            postid= random.randint(1,100)
            f.write("insert into groupPosts (groupId ,postid ) values('"+str(x+1)+"','"+str(postid)+"');\n")
print("creation of groupposts done")









    


