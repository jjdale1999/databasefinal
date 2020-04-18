from . import db
from werkzeug.security import generate_password_hash



class UserProfile(db.Model):
    # You can use this to change the table name. The default convention is to use
    # the class name. In this case a class name of UserProfile would create a
    # user_profile (singular) table, but if we specify __tablename__ we can change it
    # to `user_profiles` (plural) or some other name.
    __tablename__ = 'user_profiles'

    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(80))
    lname = db.Column(db.String(80))
    email = db.Column(db.String(80))
    location = db.Column(db.String(80))
    gender = db.Column(db.String(80))
    biography = db.Column(db.Text())
    photo = db.Column(db.String(80))
    created_date= db.Column(db.String(80))

    def __init__(self, fname, lname, email, location,gender,biography,photo, created_date):
        self.fname = fname
        self.lname = lname
        self.email = email
        self.location = location
        self.gender = gender
        self.biography = biography
        self.photo = photo
        self.created_date=created_date
    
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<User %r %r %r %r %r %r %r %r>' % (self.fname, self.lname, self.email, self.location,self.gender,self.biography,self.photo,self.created_date)
