import os,uuid
DATABASE = 'flasktaskr.db'
WTF_CSRF_ENABLED = True
SECRET_KEY = os.urandom(48)
basedir = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(basedir, DATABASE)

SQLALCHEMY_DATABASE_URI = "sqlite:///"+ DATABASE_PATH