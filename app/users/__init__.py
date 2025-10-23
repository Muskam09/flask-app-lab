from flask import Blueprint

users_bp = Blueprint('users', __name__,
                     url_prefix='/users',
                     template_folder='templates')

# Імпортуємо маршрути, пов'язані з цим Blueprint
from app.users import views