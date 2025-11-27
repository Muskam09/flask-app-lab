from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_migrate import Migrate
from sqlalchemy.orm import DeclarativeBase
from app.config import config_map
import os
import logging
from logging.handlers import RotatingFileHandler
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

class Base(DeclarativeBase):
  metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(model_class=Base)
migrate = Migrate()

bcrypt = Bcrypt()

login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'


def create_app(config_name=os.environ.get('FLASK_CONFIG', 'default')):
    """
    Фабрична функція для створення екземпляра додатка Flask.
    """
    app = Flask(__name__)

    app.config.from_object(config_map[config_name])

    db.init_app(app)
    migrate.init_app(app, db)

    bcrypt.init_app(app)

    login_manager.init_app(app)

    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/webapp.log', maxBytes=10240,
                                           backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Webapp startup')


    from .views import main_bp
    app.register_blueprint(main_bp)

    from app.users import users_bp
    app.register_blueprint(users_bp)

    from app.products import products_bp
    app.register_blueprint(products_bp)

    from app.posts import post_bp
    app.register_blueprint(post_bp)

    # обробник помилки 404
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404

    @app.shell_context_processor
    def make_shell_context():
        from app.posts.models import Post, Tag
        from app.users.models import User
        from app.products.models import Product, Category

        return {
            'db': db,
            'Post': Post,
            'Tag': Tag, 
            'User': User,
            'Product': Product, 
            'Category': Category
        }

    return app