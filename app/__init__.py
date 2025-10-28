from flask import Flask
import logging
from logging.handlers import RotatingFileHandler
import os

app = Flask(__name__)
app.config.from_pyfile("../config.py")
# app.config['SECRET_KEY'] = 'a-super-secret-key-12345'

# НАЛАШТУВАННЯ ЛОГЕРА (ДЛЯ ЛР5)
if not app.debug:
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

from . import views

from app.users import users_bp
app.register_blueprint(users_bp)

from app.products import products_bp
app.register_blueprint(products_bp)