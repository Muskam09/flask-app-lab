from flask import Blueprint

# Створюємо Blueprint
# 'users' - назва Blueprint
# __name__ - ім'я модуля
# url_prefix='/users' - всі маршрути цього Blueprint будуть починатися з /users
users_bp = Blueprint('users', __name__,
                     url_prefix='/users',
                     template_folder='templates')

# Імпортуємо маршрути, пов'язані з цим Blueprint
from app.users import views