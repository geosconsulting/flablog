from flask import request,url_for, flash, redirect
from datetime import datetime
from flask_login import UserMixin, current_user
from flask_security import RoleMixin
from werkzeug.security import generate_password_hash, check_password_hash

from flask_admin.contrib.sqla import ModelView
from flask_admin import expose, AdminIndexView

from app import db
from app import ma
from app import admin

from sqlalchemy import create_engine
import geoalchemy2
from sqlalchemy.ext.declarative import declarative_base


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, db.Sequence('user_id_seq'), primary_key=True, autoincrement=True)
    active = db.Column('is_active' , db.Boolean() , nullable=False , server_default='1')
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))

    roles = db.relationship('Role' , secondary='user_roles')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self , password):
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self , password):
        return check_password_hash(self.password , password)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name

# Define the UserRoles association table
    class UserRoles(db.Model):
        __tablename__ = 'user_roles'
        id = db.Column(db.Integer(), primary_key=True)
        user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
        role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))


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


class UserModelView(ModelView):

    can_create = False
    can_edit = False
    column_exclude_list = ['password' , ]
    can_delete = True

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))


class PostRoleModelView(ModelView):

    can_create = True
    can_edit = True
    can_delete = True

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))


class FLABlogAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        return super(FLABlogAdminIndexView , self).index()
        # return self.render('admin/index.html')


admin.add_view(UserModelView(User , db.session))
admin.add_view(PostRoleModelView(Role , db.session))
admin.add_view(PostRoleModelView(Post , db.session))
