import os

#environment variable
basedir = os.path.abspath(os.path.dirname(__file__))

#configuration
class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "myseckey12345"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///" +  os.path.join(basedir, "database") 
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    POST_PER_PAGE = 2

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'myemail@gmail.com'
    MAIL_PASSWORD = 'mypassword'

    
    RECAPTCHA_USE_SSL = False
    RECAPTCHA_PUBLIC_KEY ='enter_your_public_key'
    RECAPTCHA_PRIVATE_KEY ='enter_your_private_key'
    

