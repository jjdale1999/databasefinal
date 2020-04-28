from . import db
from werkzeug.security import generate_password_hash
db.engine.execute("drop table if exists addcomments")

db.engine.execute("drop table if exists comments")
db.engine.execute("drop table if exists groupposts")

db.engine.execute("drop table if exists joinsgroup")
db.engine.execute("drop table if exists groups")
db.engine.execute("drop table if exists friendship")
db.engine.execute("drop table if exists user_post_log")
db.engine.execute("drop table if exists posts")

db.engine.execute("drop table if exists addphoto")
db.engine.execute("drop table if exists gallery")
db.engine.execute("drop table if exists profiles")
db.engine.execute("drop table if exists users")


db.engine.execute("create table Users(userid SERIAL unique,firstName varchar(255),lastName varchar(255),email varchar(50),gender varchar(64),password text,primary key(userId))")

db.engine.execute("create table Profiles(profileNo SERIAL unique,userid int unique,profilePic int,username text,biography text,countryLiving varchar(30),primary key (userId,profileNo),foreign key(userId) references Users(userId) on delete cascade on update cascade)")
db.engine.execute("create table gallery(photoid SERIAL,photourl text,primary key (photoid) )")

db.engine.execute("create table addphoto(photoid int ,userid int ,primary key (photoid,userid), foreign key (userid) references Users(userid) on delete cascade on update cascade,foreign key (photoid) references gallery(photoid) on delete cascade on update cascade  )")

db.engine.execute("create table posts(postId SERIAL unique, content text, ctype varchar(15), postDateTime timestamp,primary key (postId))")

db.engine.execute("create table user_post_log(postId int, userid int,primary key (userId,postId),foreign key(userId) references Users(userId) on delete cascade on update cascade)")

db.engine.execute("create table Friendship(userid int,fuserid int,fType varchar(255),primary key(userId,fUserId),foreign key (userId) references Users(userId) on delete cascade on update cascade,foreign key (fuserId) references Users(userId) on delete cascade on update cascade)")

db.engine.execute("create table groups(groupId SERIAL,groupName varchar(255),createdBy varchar(255),createddate timestamp,primary key(groupId))")

db.engine.execute("create table joinsGroup(groupId int,userid int,status varchar(255),joindate timestamp,primary key(groupId,userId),foreign key(groupId) references groups(groupId) on delete cascade on update cascade,foreign key(userId) references Users(userId) on delete cascade on update cascade)")

db.engine.execute("create table groupPosts(groupId int,postid int,primary key(groupId,postid),foreign key(groupId) references groups(groupId) on delete cascade on update cascade,foreign key(postId) references posts(postId) on delete cascade on update cascade)")

db.engine.execute("create table comments(commentId SERIAL,commentDetail varchar(255),commentDateTime timestamp,primary key (commentId) )")

db.engine.execute("create table addcomments(commentId int,postId int,userid int,primary key(commentId,postId))")



# Edited
#Tables trigger based

# db.engine.execute("create table friendFrom(fUserId varchar(20),notif varchar(20),createDate date")

# db.engine.execute("create table capacity(almostFullGroup varchar(20),groupNotif varchar(100)")

# create the 3 or more procedures
# # command use to insert data into postgres
# # \i /Users/jordannedale/Desktop/databasefinal/database.sql

#Can scrap these if you don't like them I can think of others but after all the changes
#(First Trigger)Trigger shoing "Date of Friendshp"
#(Second Trigger)Trigger showing Group capacity
# """
# Delimiter $$
# create trigger friend_Time
# after insert on Friendship
# for each ROW
# BEGIN
# insert into friendFrom(fUserId,notif,createDate) values(new.fUserId,"Friends Since",FROM_UNIXTIME(
#         UNIX_TIMESTAMP('2018-01-11 12:00:00') + FLOOR(0 + (RAND() * 63072000))));
    
# END $$
# delimiter ;    




# Delimiter $$

# create trigger group_limit
# after insert on joinsGroup
# for each ROW

# insert into capacity(almostFullGroup,groupNotif) values (new.groupId," Less 50 slots remaining") if(select count(userId) from joinsGroup) >=950 and (select count(userId) from joinsGroup) <=990
# insert into capacity(almostFullGroup,groupNotif) values (new.groupId," Less 10 slots remaining") if(select count(userId) from joinsGroup) >=990 and (select count(userId) from joinsGroup) <=999
# END $$
# delimiter ;

# /*Nvm, remove two you made so paul/monique can make two*/
# """