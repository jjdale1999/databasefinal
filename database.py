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
def padding(number):
    # while(len(number)!=500002):
    #     number="0"+str(number)
    newnumber=number.zfill(50000)

    return newnumber
def postidpadding(number):
    while(len(number)!=3000002):
        number="0"+str(number)
    return number
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

    biography=fake.text()
    
    # appending to text file
    biography.replace('\r','')
    userid=padding(str(userid))
    f.write("insert into Users values('"+firstname+"','"+lastname+"','"+email+"','"+gender+"','"+password+"'); \n")

    f.write("insert into Profiles values('"+str(userid)+"','"+profilepic+"','"+username+"','"+biography+"','"+country+"');\n")

   
    print(str(i)+"\n")
print(" creation of users and profiles done")


textId=1
imageId=1
commentId=1
#creation of 3000000 posts 
for x in range(30):

    #selecting the userid for the post 
    postId=x
    userId=random.randint(1,50)
    userId=padding(str(userId))
    date_time=fake.date_time_this_decade()
    postDate=fake.date_this_year(before_today=True, after_today=False)
    postTime=fake.time()
    #even for text - odd for post
    text_photo=random.randint(0,20)

# insert into post 
    f.write("insert into posts values('"+str(userId)+"','"+str(postDate)+"','"+postTime+"');\n");

    if(text_photo%2==0):
        textpost= fake.text()
        textpost.replace('\r','')
        # insertinto text
        f.write("insert into texts values('"+str(postId)+"','"+textpost+"');\n");

        textId+=1

    else:
        photopost=fake.image_url()
        while("placeimg" not in photopost):
            photopost=fake.image_url()
        f.write("insert into images values('"+str(postId)+"','"+photopost+"');\n");

        imageId+=1

        #insert into image

    


    #creation of at least 2-40 comments on post
    randnum=random.randint(2,40)
    for y in range(randnum):
        # userid of comment
        cuserid=random.randint(1,50)
        cuserid=padding(str(cuserid))
        while(userid==cuserid):
            cuserid=random.randint(1,50)
            cuserid=padding(str(cuserid))
        commmentDetail=fake.text(max_nb_chars=150, ext_word_list=None)
        commmentDetail.replace('\r','')
        cdate_time=fake.date_time_this_decade()
        commentDate=fake.date_this_year(before_today=True, after_today=False)
        comentTime=fake.time()
        # insert into comments 
        f.write("insert into comments values('"+str(postId)+"','"+str(cuserid)+"','"+commmentDetail+"','"+str(commentDate)+"','"+comentTime+"');\n");

        commentId+=1
        #likes
        # for z in 
print(" creation of post and comments done")




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
        f.write("insert into Friendship values('"+str(x+1)+"','"+str(friendid)+"','"+fType+"');\n");


    print(x)
print(" creation of friendships done")


#create groups
users=[]
status_all=["Editor","Viewer"]
for x in range(50):
    groupId=x
    groupName=fake.word()
    createdBy= random.randint(1,50)
    f.write("insert into groups values('"+groupName+"','"+str(createdBy)+"');\n");

    randnum=random.randint(2,5)
    for x in range(randnum):
        userId=random.randint(1,50)
        userId=padding(str(userId))
        while((createdBy==userId) or (userId in users)):
            userId=random.randint(1,50)
            userId=padding(str(userId))
        users.append(userId)
        status=random.choice(status_all)

        f.write("insert into joinsGroup values('"+str(userId)+"','"+status+"');\n");


print(" creation of groups done")

    


