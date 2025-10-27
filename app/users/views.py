from flask import (
    request, redirect, url_for, render_template,
      session, flash, make_response, abort
      )
from app.users import users_bp
from datetime import datetime

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
VALID_PASSWORD = "123"

@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Сторінка логіну."""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == VALID_USERNAME and password == VALID_PASSWORD:
            session['username'] = username
            flash(f'Ласкаво просимо, {username}!', 'success')
            return redirect(url_for('users.profile'))
        else:
            flash('Неправильне ім\'я користувача або пароль! Спробуйте ще.', 'danger')
            return redirect(url_for('users.login'))

    return render_template('users/login.html')


@users_bp.route('/logout')
def logout():
    """Вихід з системи."""
    session.pop('username', None)
    flash('Ви вийшли з системи.', 'info')
    return redirect(url_for('users.login'))

@users_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    """Сторінка профілю."""
    if 'username' not in session:
        flash('Ви повинні увійти, щоб побачити цю сторінку.', 'warning')
        return redirect(url_for('users.login'))

    username = session.get('username')
    
    # --- ЗАВДАННЯ 2: КЕРУВАННЯ COOKIES ---
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
    max_age = 60 * 60 * 24 * 30 # 30 днів у секундах
    resp.set_cookie('color_scheme', theme, max_age=max_age)
    flash(f'Тему змінено на "{theme}"!', 'info')
    return resp
