from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_admin import Admin
from flask_fontawesome import FontAwesome
from flask_marshmallow import Marshmallow
from flask_restful import Api
from flasgger import Swagger
from flask_ckeditor import CKEditor
from flask_mail import Mail
import logging
from logging.handlers import SMTPHandler
from logging.handlers import RotatingFileHandler
import os

from . import config

db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()
login = LoginManager()
ma = Marshmallow()
api = Api()
swagger = Swagger()
ckeditor = CKEditor()
mail = Mail()
admin = Admin()

from flask_admin import expose, AdminIndexView


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config.DevelopmentConfig)

    if not app.debug:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'] , app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                    mailhost=(app.config['MAIL_SERVER'] , app.config['MAIL_PORT']) ,
                    fromaddr='no-reply@' + app.config['MAIL_SERVER'] ,
                    toaddrs=app.config['ADMINS'] ,
                    subject='Fabio Lana Blog Failure' ,
                    credentials=auth , secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/microblog.log' , maxBytes=10240 ,
                                           backupCount=10)
        file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Fabio Lana Blog startup')

    # DB Section
    from app import models

    db.init_app(app)
    migrate.init_app(app , db)
    bootstrap.init_app(app)
    FontAwesome(app)

    # ADMIN Section
    admin.init_app(app)
    admin.name = 'FlaBlog Admin'
    admin.template_mode = 'bootstrap3'
    admin.index_view = models.FLABlogAdminIndexView()
    admin.base_template = 'master_admin.html'

    # Main Content Section
    from .main_dir import routes
    from app.main_dir import main_bp
    app.register_blueprint(main_bp)

    # Analytics Section
    from .analytics_dir import analytics_routes
    from app.analytics_dir import analytics_bp
    app.register_blueprint(analytics_bp)

    # Authorization Section
    login.init_app(app)

    from .auth_dir import auth_routes
    from app.auth_dir import auth_bp
    app.register_blueprint(auth_bp)

    from .blog_dir import blog_routes
    from app.blog_dir import blog_bp
    app.register_blueprint(blog_bp)

    ma.init_app(app)

    from .api_dir import api_routes
    from app.api_dir import api_bp
    api.init_app(api_bp)
    app.register_blueprint(api_bp)

    swagger.init_app(app)

    ckeditor.init_app(app)

    mail.init_app(app)

    return app
