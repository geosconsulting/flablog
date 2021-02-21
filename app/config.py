import os
from pathlib import Path
basedir = os.path.abspath(os.path.dirname(__file__))
app_dir = Path(__file__).parent.parent


class Config(object):

    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'affattappelloso'

    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:antarone@localhost/flablog'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(app_dir,'instance', 'flablog.sqlite')
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # set optional bootswatch theme
    FLASK_ADMIN_SWATCH = 'cerulean'

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    ADMINS = ['fabio_100264@yahoo.it']


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
