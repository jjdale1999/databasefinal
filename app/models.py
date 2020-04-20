from . import db
from werkzeug.security import generate_password_hash


db.engine.execute("create table Users(userId varchar(20),firstName varchar(20),lastName varchar(20),email varchar(50),gender varchar(64),password text,primary key(userId))")

db.engine.execute("create table Profiles(userId varchar(20),profileNo varchar(20),profilePic text,biography text,countryLiving varchar(30),primary key (userId,profileNo),foreign key(userId) references Users(userId) on delete cascade)")

db.engine.execute("create table posts(userId varchar(20),postId varchar(20),postDate DATE,postTime time,primary key (userId,postId),foreign key(userId) references Users(userId) on delete cascade)")

# db.engine.execute("create table images(postId varchar(20),imageId varchar(20),images text,primary key(postId,imageId),foreign key(postId) references posts(postId) on delete cascade )")

# db.engine.execute("create table texts(postId varchar(20),textId varchar(20),images text,primary key(postId,textId),foreign key(postId) references posts(postId) on delete cascade )")

db.engine.execute("create table Friendship(userId varchar(20),fUserId varchar(20),fType varchar(20),primary key(userId,fUserId),foreign key (userId) references Users(userId) on delete cascade )")

db.engine.execute("create table myBookGroup(groupId varchar(20),groupName varchar(20),createdBy varchar(20),primary key(groupId))")

db.engine.execute("create table joinsGroup(groupId varchar(20),userId varchar(20),groupContentViewer varchar(20),groupContentEditor varchar(20),primary key(groupId,userId),foreign key(groupId) references myBookGroup(groupId) on delete cascade,foreign key(userId) references Users(userId))")

# db.engine.execute("create table comments(userId varchar(20),postId varchar(20),commentId varchar(20),commentDetail varchar(20),commentDate date,comentTime time,primary key (userId,commentId,postId),foreign key (userId) references Users(userId) on delete cascade,foreign key (postId) references posts(postId) on delete cascade )")

# command use to insert data into postgres
# \i /Users/jordannedale/Desktop/databasefinal/database.sql 
