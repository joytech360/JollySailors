import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv()

class Config(object):
	SECRET_KEY = os.getenv('SECRET_KEY')
	SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	MAIL_SERVER = os.getenv('MAIL_SERVER')
	MAIL_PORT = int(os.getenv('MAIL_PORT') or 25)
	MAIL_USE_TLS = os.getenv('MAIL_USE_TLS') is not None
	MAIL_USERNAME = os.getenv('MAIL_USERNAME')
	MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
	ADMINS = os.getenv('ADMINS')
	UPLOADED_PHOTOS_DEST = os.getcwd() + '/app/static/uploads'