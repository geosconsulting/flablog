from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app import login
from app import ma

from sqlalchemy import create_engine
import geoalchemy2
from sqlalchemy.ext.declarative import declarative_base

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, db.Sequence('user_id_seq'), primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self , password):
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self , password):
        return check_password_hash(self.password , password)

class Post(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "username", "email")
        model = User

user_schema = UserSchema()
users_schema = UserSchema(many=True)

sparc_engine = create_engine('postgresql://fabiolana:antarone@localhost:5432/sparc')
Base = declarative_base()
Base.metadata.reflect(sparc_engine)


class Flood(Base):
    __table__ = Base.metadata.tables['annual_pop_flood']

class FloodSchema(ma.Schema):
    class Meta:
        fields = ("id","iso3", "adm0_name", "rp25", "rp50","rp100","rp200","rp500","rp1000")
        model = Flood


flood_schema = FloodSchema()
floods_schema = FloodSchema(many=True)

class EmdatFlood(Base):
    __table__ = Base.metadata.tables['flood_emdat']

class FloodEmdatSchema(ma.Schema):
    class Meta:
        fields = ("id","country", "location", "type", "killed", "total_affected")
        model = EmdatFlood

flood_emdat_schema = FloodEmdatSchema()
floods_emdat_schema = FloodEmdatSchema(many=True)