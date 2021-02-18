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
