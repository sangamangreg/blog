import datetime
from app import db
from app.models.models import MyModel


class Attachment( MyModel ):
    __tablename__ = 'attachments'

    id = db.Column( db.Integer, primary_key=True )
    name = db.Column( db.String( 64 ), nullable=False )
    mime_type = db.Column( db.String( 64 ) )
    extension = db.Column( db.String( 64 ) )
    file_url = db.Column( db.Text )
    owner_id = db.Column( db.Integer, db.ForeignKey( 'users.id' ) )
    created_at = db.Column( db.DateTime, default=datetime.datetime.utcnow )

    def __init__(self, name, mime_type, extension, file_url, owner_id):
        self.name = name
        self.mime_type = mime_type
        self.extension = extension
        self.file_url = file_url
        self.owner_id = owner_id
