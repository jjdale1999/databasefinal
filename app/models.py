from . import db
from werkzeug.security import generate_password_hash

db.engine.execute("drop table if exists comments")
db.engine.execute("drop table if exists joinsgroup")
db.engine.execute("drop table if exists groups")
db.engine.execute("drop table if exists friendship")
db.engine.execute("drop table if exists images")
db.engine.execute("drop table if exists texts")
db.engine.execute("drop table if exists posts")
db.engine.execute("drop table if exists profiles")
db.engine.execute("drop table if exists users")

db.engine.execute("create table Users(userid SERIAL unique,firstName varchar(255),lastName varchar(255),email varchar(50),gender varchar(64),password text,primary key(userId))")

db.engine.execute("create table Profiles(userid int unique,profileNo SERIAL unique,profilePic text,username text,biography text,countryLiving varchar(30),primary key (userId,profileNo),foreign key(userId) references Users(userId) on delete cascade on update cascade)")

db.engine.execute("create table posts( postId SERIAL unique, userid int ,postDate text,postTime text,primary key (userId,postId),foreign key(userId) references Users(userId) on delete cascade on update cascade)")

db.engine.execute("create table images(postId int ,imageId SERIAL,images text,primary key(postId,imageId),foreign key(postId) references posts(postId) on delete cascade on update cascade)")

db.engine.execute("create table texts(postId int unique ,textId SERIAL unique,images text,primary key(postId,textId),foreign key(postId) references posts(postId) on delete cascade on update cascade)")

db.engine.execute("create table Friendship(userid int,fuserid int,fType varchar(255),primary key(userId,fUserId),foreign key (userId) references Users(userId) on delete cascade on update cascade)")

db.engine.execute("create table groups(groupId SERIAL,groupName varchar(255),createdBy varchar(255),primary key(groupId))")

db.engine.execute("create table joinsGroup(groupId SERIAL,userid int,groupContentViewer varchar(255),groupContentEditor varchar(255),primary key(groupId,userId),foreign key(groupId) references groups(groupId) on delete cascade on update cascade,foreign key(userId) references Users(userId) on delete cascade on update cascade)")

db.engine.execute("create table comments(postId int ,commentId SERIAL,  userid int,commentDetail varchar(255),commentDate text,comentTime text,primary key (userId,commentId,postId),foreign key (userId) references Users(userId) on delete cascade on update cascade,foreign key (postId) references posts(postId) on delete cascade on update cascade )")


# create the 3 or more procedures
# # command use to insert data into postgres
# # \i /Users/jordannedale/Desktop/databasefinal/database.sql 
