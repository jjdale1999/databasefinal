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

#creation of each user and profiles
f= open("database.sql","w+")
for i in range(50):
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

    profilepic=fake.image_url()
    password=fake.password(length=40, special_chars=True, upper_case=True)
    while("placeimg" not in profilepic):
        profilepic=fake.image_url()

    biography=fake.text(max_nb_chars=255, ext_word_list=None)
    
    # appending to text file
    f.write("insert into Users values('"+"US"+str(userid)+"','"+firstname+"','"+lastname+"','"+email+"','"+gender+"','"+password+"'); \n")
  
    f.write("insert into Profiles values('"+"US"+str(userid)+"','"+"PF"+str(profileNo)+"','"+profilepic+"','"+biography+"','"+country+"');\n")
    print(str(i)+"\n")
print(" creation of users and profiles done")


textId=1
imageId=1
commentId=1
#creation of 3000000 posts 
# for x in range(30):

#     #selecting the userid for the post 
#     postId=x
#     userId=random.randint(1,50)
#     date_time=fake.date_time_this_decade()
#     postDate=fake.date_this_year(before_today=True, after_today=False)
#     postTime=fake.time()
#     #even for text - odd for post
#     text_photo=random.randint(0,20)

#     if(text_photo%2==0):
#         textpost= fake.text()
#         # insertinto text
#         f.write("insert into text values('"+"PS"+str(postId)+"','"+"TT"+str(textId)+"','"+textpost+"');\n");
#         textId+=1

#     else:
#         photopost=fake.image_url()
#         while("placeimg" not in photopost):
#             photopost=fake.image_url()
#         f.write("insert into image values('"+"PS"+str(postId)+"','"+"IM"+str(imageId)+"','"+photopost+"');\n");
#         imageId+=1

#         #insert into image

#     # insert into post 
#     f.write("insert into post values('"+"PS"+str(postId)+"','"+"US"+str(userId)+"','"+str(postDate)+"','"+postTime+"');\n");


#     #creation of at least 2-40 comments on post
#     randnum=random.randint(2,40)
#     for y in range(randnum):
#         # userid of comment
#         cuserid=random.randint(1,50)
#         while(userid==cuserid):
#             cuserid=random.randint(1,50)
#         commmentDetail=fake.text(max_nb_chars=150, ext_word_list=None)
#         cdate_time=fake.date_time_this_decade()
#         commentDate=fake.date_this_year(before_today=True, after_today=False)
#         comentTime=fake.time()
#         # insert into comments 
#         f.write("insert into comment values('"+"CM"+str(commentId)+"','"+"US"+str(cuserid)+"','"+commmentDetail+"','"+str(commentDate)+"','"+comentTime+"');\n");
#         commentId+=1
#         #likes
#         # for z in 
# print(" creation of post and comments done")




# friends 
for x in range(50):
    # creation of friends
    friends=[]
    relationships=["Relatives", "School", "Work"]

    randnum=random.randint(0,5)
    for y in range(randnum):
        friendid=random.randint(1,50)
        while((friendid==x) or (friendid in friends)):
            friendid=random.randint(1,50)
        fType=random.choice(relationships)

        friends.append(friendid)
        f.write("insert into Friendship values('"+"US"+str(x)+"','"+"US"+str(friendid)+"','"+fType+"');\n");

    print(x)
print(" creation of friendships done")


#create groups
users=[]
status_all=["Editor","Viewer"]
for x in range(50):
    groupId=x
    groupName=fake.word()
    createdBy= random.randint(1,50)
    f.write("insert into myBookGroup values('"+"GP"+str(groupId)+"','"+groupName+"','"+"US"+str(createdBy)+"');\n");

    randnum=random.randint(2,5)
    for x in range(randnum):
        userId=random.randint(1,50)
        while((createdBy==userId) or (userId in users)):
            userId=random.randint(1,50)
        users.append(userId)
        status=random.choice(status_all)

        f.write("insert into joinsGroup values('"+"GP"+str(groupId)+"','"+"US"+str(userId)+"','"+status+"');\n");


print(" creation of groups done")

    


