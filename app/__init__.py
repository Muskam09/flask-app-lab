from flask import Flask

app = Flask(__name__)
app.config.from_pyfile("../config.py")
# app.config['SECRET_KEY'] = 'a-super-secret-key-12345'

from . import views

from app.users import users_bp
app.register_blueprint(users_bp)

from app.products import products_bp
app.register_blueprint(products_bp)