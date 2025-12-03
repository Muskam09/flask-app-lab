import secrets
import os
from flask import (
    request, redirect, url_for, render_template,
    session, flash, make_response, abort, Blueprint, current_app
)
from datetime import datetime, timezone
from app import db
from app.users.models import User
from app.forms import LoginForm
from app.users.forms import RegistrationForm, UpdateAccountForm
from flask_login import login_user, current_user, logout_user, login_required
from app.users import users_bp
from PIL import Image

@users_bp.route("/hi/<string:name>")
def greetings(name):
    name = name.upper()
    age = request.args.get("age", None, int)
    return render_template("users/hi.html", name=name, age=age)

@users_bp.route("/admin")
def admin():
    to_url = url_for("users.greetings", name="administrator", age=45)
    print(f"Redirecting to: {to_url}")
    return redirect(to_url)

VALID_USERNAME = "admin"
VALID_PASSWORD = "123456"

# ===== ЛОГІН =====
@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('posts.list_all'))

    form = LoginForm()

    if form.validate_on_submit():
        # Шукаємо користувача в базі даних
        user = db.session.scalar(db.select(User).where(User.username == form.username.data))

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'Вітаємо, {user.username}! Ви увійшли в систему.', 'success')

            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('users.account'))
        else:
            flash('Вхід не вдався. Перевірте ім\'я та пароль.', 'danger')

    return render_template('users/login.html', form=form)

# ===== РЕЄСТРАЦІЯ =====
@users_bp.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('posts.list_all'))
    
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash(f'Акаунт створено для {form.username.data}!', 'success')
        return redirect(url_for('users.login'))

    return render_template('users/register.html', title='Register', form=form)

# ===== ВИХІД =====
@users_bp.route('/logout')
def logout():
    logout_user()
    flash('Ви вийшли з системи.', 'info')
    return redirect(url_for('users.login'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext

    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path)
    
    return picture_fn

@users_bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()

# ===== ACCOUNT (Профіль користувача) =====
@users_bp.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        # Оновлюємо інші дані
        current_user.username = form.username.data
        current_user.email = form.email.data

        current_user.about_me = form.about_me.data

        db.session.commit()
        flash('Ваш акаунт оновлено!', 'success')
        return redirect(url_for('users.account'))
        
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('users/account.html', title='Account', image_file=image_file, form=form)

# ===== PROFILE (Стара сторінка з Cookies) =====
@users_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """Сторінка керування кукі."""

    username = current_user.username

    if request.method == 'POST':
        # 1. Додавання кукі
        if 'add_cookie' in request.form:
            key = request.form.get('cookie_key')
            value = request.form.get('cookie_value')
            expiry = request.form.get('cookie_expiry')
            
            if key and value:
                resp = make_response(redirect(url_for('users.profile')))
                if expiry:
                    max_age = int(expiry) * 60
                    resp.set_cookie(key, value, max_age=max_age)
                else:
                    resp.set_cookie(key, value)
                flash(f'Кукі "{key}" додано!', 'success')
                return resp

        # 2. Видалення кукі за ключем
        elif 'delete_cookie' in request.form:
            key_to_delete = request.form.get('delete_key')
            if key_to_delete:
                resp = make_response(redirect(url_for('users.profile')))
                resp.delete_cookie(key_to_delete)
                flash(f'Кукі "{key_to_delete}" видалено!', 'info')
                return resp

        # 3. Видалення всіх кукі
        elif 'delete_all_cookies' in request.form:
            resp = make_response(redirect(url_for('users.profile')))
            for key in request.cookies:
                if key != 'session': # Не чіпаємо сесію
                    resp.delete_cookie(key)
            flash('Всі кукі (окрім сесії) видалено!', 'info')
            return resp

    cookies = request.cookies
    return render_template('users/profile.html', username=username, cookies=cookies)

@users_bp.route('/set-color/<theme>')
def set_color(theme):
    """Зберігає вибір теми у кукі."""
    resp = make_response(redirect(url_for('users.profile')))
    max_age = 60 * 60 * 24 * 30 
    resp.set_cookie('color_scheme', theme, max_age=max_age)
    flash(f'Тему змінено на "{theme}"!', 'info')
    return resp

@users_bp.route("/users")
@login_required  # Вимога: доступ тільки для авторизованих
def users_list():
    users = db.session.scalars(db.select(User)).all()

    users_count = len(users)
    
    return render_template('users/users_list.html', users=users, count=users_count)