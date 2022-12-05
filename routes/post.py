from flask import request, redirect, render_template, url_for, flash
from flask_login import login_required, current_user
from app import app, db
from models.models import *


@app.route('/users/create-post', methods=["GET", "POST"])
@login_required
def create_post():
    post_id = request.form.get('post_id')
    user_id = current_user.get_id()
    categor = request.form.get('categor')
    topic = request.form.get('topic')
    text = request.form.get('text')
    date_add = request.form.get('date_add')

    if request.method == 'POST':
        if len(topic) <= 6:
            flash("Тема має містити мінімум 7 символів", category='error')
            return redirect(url_for('create_post'))
        if len(text) <= 4:
            flash("Введіть текст поста мінімум 5 символів)", category='error')
            return redirect(url_for('create_post'))
        else:
            post = Posts(
                post_id=post_id,
                user_id=user_id,
                categor=categor,
                topic=topic,
                text=text,
                date_add=date_add
            )
            try:
                db.session.add(post)
                db.session.commit()
                flash("Пост добавлено успішно", category='success')
                return redirect("/")
            except:
                flash("Невідома помилка при добавлянні поста", category='error')
                return redirect(url_for('create_post'))

    else:
        return render_template('create-post.html')


@app.route("/users/my-post", methods=["GET"])
@login_required
def my_post():
    user_id = current_user.get_id()
    post = Posts.query.filter(Posts.user_id == user_id)
    all_post = post.all()
    return render_template("my-post.html", post=all_post)


@app.route("/users/my-post/post:<post_id>", methods=["GET", "POST"])
@login_required
def post_detail(post_id):
    detail = Posts.query.get(post_id)
    return render_template("post_detail.html", detail=detail)


@app.route("/users/my-post/post:<post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    detail = Posts.query.get(post_id)
    if request.method == 'POST':
        detail.topic = request.form['topic']
        detail.text = request.form['text']
        try:
            db.session.commit()
            flash("Пост успішно редаговано", category='success')
            return redirect(url_for("my_post"))
        except:
            flash("При редагуванні сталась помилка", category='error')
            return redirect(url_for("update_post"))

    else:
        return render_template('update_post.html', detail=detail)


@app.route('/users/my-post/post:<post_id>/delete')
@login_required
def delete_post(post_id):
    post = Posts.query.get_or_404(post_id)
    try:
        db.session.delete(post)
        db.session.commit()
        flash("Пост видалено успішно", category='success')
        return redirect('/users/my-post')
    except:
        flash("Помилка видалення")
        return redirect('/users/my-post/post:<post_id>')


@app.route('/post:<post_id>/<action>')
@login_required
def like_action(post_id, action):
    post = Posts.query.filter_by(post_id=post_id).first_or_404()
    if action == 'like':
        current_user.like_post(post)
        db.session.commit()
    if action == 'unlike':
        current_user.unlike_post(post)
        db.session.commit()
    return redirect(request.referrer)
