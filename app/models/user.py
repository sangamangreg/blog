import datetime
from enum import Enum
from flask_login import UserMixin
from app import login_manager, db
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

from app.models.models import MyModel


@login_manager.user_loader
def load_user(user_id):
    return User.query.get( user_id )


class Role( Enum ):
    SUPERUSER = "SUPERUSER"
    USER = "USER"


class ReseetPassword( MyModel ):
    __tablename__ = 'reset_password'

    id = db.Column( db.Integer, primary_key=True )
    owner_id = db.Column( db.Integer, db.ForeignKey('users.id') )
    link_hashed = db.Column( db.String( 128 ), index=True )

    def __init__(self, user_id):
        self.owner_id = user_id
        self.link_hashed = str(uuid.uuid4())

    def check_link_hashed(self, link_hashed):
        return ReseetPassword.query.filter_by(link_hashed=link_hashed).first()

class User( MyModel ):
    __tablename__ = 'users'

    id = db.Column( db.Integer, primary_key=True )
    name = db.Column( db.String( 64 ), nullable=False )
    username = db.Column( db.String( 255 ), unique=True, index=True )
    email = db.Column( db.String( 255 ), unique=True, index=True )
    phone = db.Column( db.Integer(), nullable=True )
    password_hashed = db.Column( db.String( 128 ) )
    role = db.Column( db.Enum( Role ) )
    active = db.Column( db.Boolean, default=True )
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, name, username, email, phone, password, role=None):
        self.name = name
        self.username = username
        self.email = email
        self.phone = phone
        self.password_hashed = self.set_password(password)

        if not role:
            self.role = Role.USER

    def set_password(self, password):
        self.password_hashed = generate_password_hash( password )

    def check_password(self, password):
        print(generate_password_hash(password))
        return check_password_hash(self.password_hashed, password)

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_by_username(username):
        return User.query.filter_by( username=username ).first()

    @staticmethod
    def get(id):
        return User.query.get(id)