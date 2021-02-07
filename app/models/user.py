import datetime
from enum import Enum
from flask_login import UserMixin
from app import login_manager, db
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(user_id):
    return User.query.get( user_id )


class Role( Enum ):
    SUPERUSER = "SUPERUSER"
    USER = "USER"


class User( UserMixin, db.Model ):
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
        self.password_hashed = generate_password_hash( password )

        if not role:
            self.role = Role.USER

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_by_username(username):
        return User.query.filter_by( username=username ).first()