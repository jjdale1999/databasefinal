from . import db
from werkzeug.security import generate_password_hash







db.engine.execute("drop table comments")
db.engine.execute("drop table joinsgroup")
db.engine.execute("drop table groups")
db.engine.execute("drop table friendship")
db.engine.execute("drop table images")
db.engine.execute("drop table texts")
db.engine.execute("drop table posts")
db.engine.execute("drop table profiles")
db.engine.execute("drop table users")

db.engine.execute("create table Users(userId varchar(255) unique,firstName varchar(255),lastName varchar(255),email varchar(50),gender varchar(64),password text,primary key(userId))")

db.engine.execute("create table Profiles(userId varchar(255) unique,profileNo varchar(255) unique,profilePic text,username text,biography text,countryLiving varchar(30),primary key (userId,profileNo),foreign key(userId) references Users(userId) on delete cascade)")

db.engine.execute("create table posts( postId varchar(255) unique, userId varchar(255) ,postDate text,postTime text,primary key (userId,postId),foreign key(userId) references Users(userId) on delete cascade)")

db.engine.execute("create table images(postId varchar(255),imageId varchar(255),images text,primary key(postId,imageId),foreign key(postId) references posts(postId) on delete cascade )")

db.engine.execute("create table texts(postId varchar(255) unique ,textId varchar(255)unique,images text,primary key(postId,textId),foreign key(postId) references posts(postId) on delete cascade )")

db.engine.execute("create table Friendship(userId varchar(255),fUserId varchar(255),fType varchar(255),primary key(userId,fUserId),foreign key (userId) references Users(userId) on delete cascade )")

db.engine.execute("create table groups(groupId varchar(255),groupName varchar(255),createdBy varchar(255),primary key(groupId))")

db.engine.execute("create table joinsGroup(groupId varchar(255),userId varchar(255),groupContentViewer varchar(255),groupContentEditor varchar(255),primary key(groupId,userId),foreign key(groupId) references groups(groupId) on delete cascade,foreign key(userId) references Users(userId))")

db.engine.execute("create table comments(postId varchar(255),commentId varchar(255),  userId varchar(255),commentDetail varchar(255),commentDate text,comentTime text,primary key (userId,commentId,postId),foreign key (userId) references Users(userId) on delete cascade,foreign key (postId) references posts(postId) on delete cascade )")

# # command use to insert data into postgres
# # \i /Users/jordannedale/Desktop/databasefinal/database.sql 
