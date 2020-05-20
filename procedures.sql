CREATE PROCEDURE addlike(postid integer, userid integer)
LANGUAGE sql
AS $$
	insert into likes values(postid,userid);
$$;

CREATE PROCEDURE addfriend(userid integer, followerid integer,ftype varchar(20))
LANGUAGE sql
AS $$
	insert into Friendship (userid,fuserid,ftype) values(userid,followerid,ftype);
$$;
CREATE PROCEDURE addphotos(photoid integer, userid integer)
LANGUAGE sql
AS $$
	insert into addphoto (photoid,userid) values(photoid,userid);
$$;
CREATE PROCEDURE adduserposts(postid integer, userid integer)
LANGUAGE sql
AS $$
	insert into user_post_log (postid,userid) values(postid,userid);
$$;
