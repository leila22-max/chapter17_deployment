import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    """Define app configurations"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard-to-guess'

    #Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'app.db')
    SQALCHEMY_TRACK_MODIFICATIONS = False

    #Email configurations
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = os.environ.get('ADMINS')

    # Pagination
    POSTS_PER_PAGE = int(os.environ.get('POSTS_PER_PAGE'))