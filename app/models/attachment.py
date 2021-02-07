import datetime
from enum import Enum
from flask_login import UserMixin
from sqlalchemy.ext.mutable import MutableList

from app import db


class Attachment( UserMixin, db.Model ):
    __tablename__ = 'attachments'

    id = db.Column( db.Integer, primary_key=True )
    name = db.Column( db.String(64), nullable=False )
    mime_type = db.Column( db.String(64))
    extension = db.Column( db.String( 64 ) )
    file_url = db.Column( db.Text )
    owner_id = db.Column( db.Integer, db.ForeignKey('users.id') )
    created_at = db.Column( db.DateTime, default=datetime.datetime.utcnow )

    def __init__(self):
        pass