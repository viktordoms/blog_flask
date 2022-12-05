from flask import flash, redirect, request, url_for, render_template
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash

from models.models import Users, Posts
from app import app, login_manager, db
from routes.main import *
from models.UserLogin import *


@app.route('/users/exit', methods=["GET", "POST"])
def login():
     email = request.form.get("email")
     password = request.form.get("password")

     if current_user.is_authenticated:
         return redirect("/users")

     if email and password:
         user = Users.query.filter_by(email=email).first()
         if user and check_password_hash(user.password, password):
             rm = True if request.form.get("remainme") else False
             login_user(user, remember=rm)
             flash('Авторизація успішна', category='success')
             return redirect(url_for('users'))
         else:
             flash("Помилка.Перевірте логін або пароль", category='error')
             return redirect(url_for("login"))
     else:
         return render_template('login.html')


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    flash("Ви вийшли з акаунта", category='success')
    logout_user()
    return redirect(url_for('main_page'))


@app.after_request
def redirect_to_singin(response):
    if response.status_code == 401:
        flash("Для виконання даної дії потріно авторизуватись", category='error')
        return redirect(url_for('login') + "?next" + request.url)
    return response


@login_manager.user_loader
def load_user(id):
    return Users.query.get(id)


@app.route("/users/")
@login_required
def users():
    user_id = current_user.get_id()
    return render_template("user_page.html", user_id=user_id, name=current_user)


