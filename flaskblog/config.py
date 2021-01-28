import os

class Config:
    SECRET_KEY = os.environ.get('FLASKBLOG_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('FLASK_BLOG_SQLALCHEMY_DATABASE_URI')
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
