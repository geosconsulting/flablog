from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_fontawesome import FontAwesome
from flask_marshmallow import Marshmallow
from flask_restful import Api
from flasgger import Swagger
from flask_ckeditor import CKEditor

from . import config

db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()
login = LoginManager()
ma = Marshmallow()
api = Api()
swagger = Swagger()
ckeditor = CKEditor()


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config.DevelopmentConfig)

    # DB Section
    from app import models

    db.init_app(app)
    migrate.init_app(app , db)
    bootstrap.init_app(app)
    FontAwesome(app)

    # ADMIN Section
    admin = Admin(app , name='Fabio Lana Blog' , template_mode='bootstrap3')
    admin.add_view(ModelView(models.User , db.session))
    admin.add_view(ModelView(models.Post , db.session))


    # Main Content Section
    from .main_dir import routes
    from app.main_dir import main_bp
    app.register_blueprint(main_bp)

    # Analytics Section
    from .analytics_dir import analytics_routes
    from app.analytics_dir import analytics_bp
    app.register_blueprint(analytics_bp)

    #Authorization Section
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

    return app
