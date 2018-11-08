import os

SECRET_KEY= 'never-guess'
SECURITY_PASSWORD_SALT = 'hard-to-guess'
DEBUG = True
DB_USER_NAME ='root'
DB_PASSWORD ='hassan'
DB_NAME = 'constology'
DB_HOST = '127.0.0.1:3306'
DB_URI ="mysql+pymysql://%s:%s@%s/%s" %(DB_USER_NAME, DB_PASSWORD, DB_HOST, DB_NAME)
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = DB_URI
POSTS_PER_PAGE = 10

# mail accounts
MAIL_DEFAULT_SENDER = 'eng.hassanemam@gmail.com'
