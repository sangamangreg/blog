from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dbpath import DB_URI


engine = create_engine(DB_URI)
Base = declarative_base()
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()

from app.models.user import User
from app.models.user import Role

from app.models.blog import Category
from app.models.blog import Blog

from app.models.attachment import Attachment




