from app import db
from flask_login import UserMixin


class MyModel(UserMixin, db.Model):
    __abstract__ = True

    def save(self):
        db.session.add(self)
        db.session.commit()