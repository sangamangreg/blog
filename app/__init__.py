from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_login import LoginManager
from flask_script import Manager
from dbpath import DB_URI

login_manager = LoginManager()
app = Flask( __name__ )
app.config['SECRET_KEY'] = 'mysecretkey'  # import from env on production
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy( app )
migrate = Migrate( app, db )

manager = Manager( app )
manager.add_command( 'db', MigrateCommand )

login_manager.init_app( app )
login_manager.login_view = 'login'

from app import models
from app.auth.views import users
from app.blog.views import blogs

app.register_blueprint(users)
app.register_blueprint(blogs)