from flask import Blueprint

users_bp = Blueprint(
    'users', 
    __name__,
    url_prefix='/users',
    template_folder='templates',
    static_folder='static',
    static_url_path='/users/static'
)

from . import views 
from . import models