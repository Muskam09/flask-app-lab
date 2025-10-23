from flask import request, redirect, url_for, render_template
# Імпортуємо наш Blueprint з файлу __init__.py у цій же папці
from app.users import users_bp

# Замість @app.route ми використовуємо @users_bp.route
# Шлях буде /users/hi/<name>
@users_bp.route("/hi/<string:name>")
def greetings(name):
    name = name.upper()
    age = request.args.get("age", None, int)
    return render_template("users/hi.html", name=name, age=age)

# Шлях буде /users/admin
@users_bp.route("/admin")
def admin():
    # Зверніть увагу на 'users.greetings'
    # 'users' - це назва Blueprint
    to_url = url_for("users.greetings", name="administrator", age=45)
    print(f"Redirecting to: {to_url}")
    return redirect(to_url)