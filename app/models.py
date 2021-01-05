from datetime import datetime
from app import db

class User(db.Model):
    userid = db.Column(db.Integer, db.Sequence('user_id_seq'), primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))
    bio = db.Column(db.Text , index=False , unique=False , nullable=True)
    admin = db.Column(db.Boolean , index=False , unique=False ,nullable=False)

    def __init__(self , userid, username , email , password, bio, admin):
        self.userid = userid
        self.username = username
        self.email = email
        self.password = password
        self.bio = bio
        self.admin = admin

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Post(db.Model):
    postid = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.userid'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)
