from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from . import config

db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config.DevelopmentConfig)

    # DB Section
    from app import models

    db.init_app(app)
    migrate.init_app(app , db)
    bootstrap.init_app(app)

    # ADMIN Section
    admin = Admin(app , name='Fabio Lana Blog' , template_mode='bootstrap3')
    admin.add_view(ModelView(models.User , db.session))
    admin.add_view(ModelView(models.Post , db.session))

    # Main Content Section
    from .main import routes
    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Analytics Section
    from .analytics import data_analytics
    from app.analytics import analytics as data_analytics
    app.register_blueprint(data_analytics)

    #Authorization Section
    # login_manager.init_app(app)

    from .auth import auth_routes
    from app.auth import auth as user_management
    app.register_blueprint(user_management)

    return app
