import datetime
from enum import Enum
from flask_login import UserMixin
from sqlalchemy.ext.mutable import MutableList
from app.models.models import MyModel
from app import db


class Status( Enum ):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"


class Category( MyModel ):
    __tablename__ = 'categories'

    id = db.Column( db.Integer, primary_key=True )
    name = db.Column( db.Text, nullable=False, unique=True )
    active = db.Column( db.Boolean, default=True )
    owner_id = db.Column( db.Integer, db.ForeignKey('users.id') )
    created_at = db.Column( db.DateTime, default=datetime.datetime.utcnow )

    def __init__(self, name, user_id):
        self.name = name
        self.owner_id = user_id


class Blog( MyModel ):
    __tablename__ = 'blogs'

    id = db.Column( db.Integer, primary_key=True )
    title = db.Column( db.Text, nullable=False )
    slug = db.Column( db.Text, unique=True )
    content = db.Column( db.Text, nullable=False )
    status = db.Column( db.Enum( Status ), default=Status.DRAFT )
    active = db.Column( db.Boolean, default=False )
    created_at = db.Column( db.DateTime, default=datetime.datetime.utcnow )

    # relations defined here
    categories = db.Column( MutableList.as_mutable(db.PickleType) )
    owner_id = db.Column( db.Integer, db.ForeignKey( 'users.id' ) )
    featured_image_id = db.Column( db.Integer, db.ForeignKey( 'attachments.id' ) )

    def __init__(self):
        pass
