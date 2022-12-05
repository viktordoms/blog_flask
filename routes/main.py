from app import app
from flask import render_template, request
from models.models import Posts, Users, PostLike
from sqlalchemy import and_, func

@app.route('/', methods=["GET"])
def main_page():
    post = Posts.query.all()
    return render_template('main.html', post=post)


@app.route("/post:<post_id>")
def post_detail_main(post_id):
    detail = Posts.query.get(post_id)
    return render_template("post_detail_main.html", detail=detail)


@app.route("/all_post/", methods=["GET", "POST"])
def all_post():
    post = Posts.query
    page = request.args.get("page")
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    pages = post.paginate(page=page, per_page=4)
    return render_template("all_post.html", post=post, pages=pages)


@app.route("/all_post/categor_post", methods=["GET", "POST"])
def categor_post():
    conditions = []
    if request.args.get('categor'):
        conditions.append(Posts.categor.like(request.args['categor']))

    if_search = Posts.query.filter(and_(*conditions))
    post_categor = if_search.all()

    return render_template("post_categor.html", post_categor=post_categor, conditions=conditions)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page404.html'), 404

