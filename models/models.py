from sqlalchemy.orm import relationship

from app import db
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy import ForeignKey


class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(500), nullable=False)

    posts = db.relationship("Posts", back_populates="users")
    liked = db.relationship('PostLike', foreign_keys='PostLike.user_id', backref='users', lazy='dynamic')

    def __repr__(self):
        return 'Users %r>' % self.id

    @property
    def serialize(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password": self.password
        }

    def like_post(self, post):
        if not self.has_liked_post(post):
            like = PostLike(user_id=self.id, post_id=post.post_id)
            db.session.add(like)

    def unlike_post(self, post):
        if self.has_liked_post(post):
            PostLike.query.filter_by(user_id=self.id, post_id=post.post_id).delete()

    def has_liked_post(self, post):
        return PostLike.query.filter(
            PostLike.user_id == self.id,
            PostLike.post_id == post.post_id).count() > 0


class Posts(db.Model):
    __tablename__ = 'posts'
    post_id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    categor = db.Column(db.String(50), nullable=False)
    topic = db.Column(db.String(250), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date_add = db.Column(db.DateTime, default=datetime.utcnow)

    likes = db.relationship('PostLike', backref='post', lazy='dynamic')
    user_id = db.Column(db.Integer, ForeignKey("users.id"), nullable=False)
    users = db.relationship("Users", back_populates="posts")

    def __repr__(self):
        return 'Posts %r>' % self.post_id

    @property
    def serialize(self):
        return {
            "post_id": self.post_id,
            "categor": self.categor,
            "topic": self.topic,
            "text": self.text,
            "date_add": self.date_add,
            "user_id": self.user_id
        }


class PostLike(db.Model):
    __tablename__ = 'post_like'
    like_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'))

    def __repr__(self):
        return 'PostLike %r>' % self.like_id

    @property
    def serialize(self):
        return {
            "like_id": self.id,
            "user_id": self.user_id,
            "post_id": self.post_id
        }
