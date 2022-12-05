from app import app, db
from flask import render_template, request, redirect, flash, url_for
from models.models import *
from werkzeug.security import generate_password_hash
from routes.login import *


@app.route('/users/new', methods=['POST', 'GET'])
def registration():
    id = request.form.get('id')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    password = request.form.get('password')
    password2 = request.form.get('password2')

    if request.method == 'POST':
        if password != password2:
            flash("Паролі не співпадають", category='error')
            return redirect(url_for('registration'))
        else:
            has_password = generate_password_hash(password)
            user = Users(
                id=id,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=has_password
            )

            try:
                db.session.add(user)
                db.session.commit()
                flash("Реєстрація пройшла успішно", category='success')
                return redirect(url_for('login'))
            except:
                 flash("Користувач з таким email вже існує", category='error')
                 return redirect(url_for('registration'))

    else:
        return render_template('registration.html')
