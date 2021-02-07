import os

basedir = os.path.abspath( os.path.dirname( __file__ ) )
DB_URI = "sqlite:///" + os.path.join( basedir, "blog.sqlite" )