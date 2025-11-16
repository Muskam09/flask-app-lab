from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import DeclarativeBase
from app.config import config_map
import os
import logging
from logging.handlers import RotatingFileHandler

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
migrate = Migrate()

def create_app(config_name=os.environ.get('FLASK_CONFIG', 'default')):
    """
    Фабрична функція для створення екземпляра додатка Flask.
    """
    app = Flask(__name__)

    app.config.from_object(config_map[config_name])

    db.init_app(app)
    migrate.init_app(app, db)

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
        from app.posts.models import Post
        return {'db': db, 'Post': Post}
    return app