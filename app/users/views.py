from flask import request, redirect, url_for, render_template
from app.users import users_bp


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