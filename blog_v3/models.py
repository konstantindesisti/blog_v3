from sqlalchemy.orm import relationship
from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy import ForeignKey


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


class BlogPost(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    author_id = db.Column(db.Integer, ForeignKey('users.id'))
    author = relationship('Users', back_populates='posts')
    comments = relationship('Comments', back_populates='blog')

    def __repr__(self):
        return (f'BlogPost(id:{self.id}|title:{self.title}|subtitle:{self.subtitle}|'
                f'date:{self.date}|body:{self.body}|author:{self.author})')


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String, nullable=False)
    posts = relationship('BlogPost', back_populates='author')
    comments = relationship('Comments', back_populates='author')

    def set_password_hash(self, entered_password):
        self.password = generate_password_hash(entered_password,salt_length=8)

    def check_pass(self, password_to_check):
        return check_password_hash(self.password, password_to_check)

    def __repr__(self):
        return f'User(id:{self.id}|email:{self.email}|name:{self.name}'


class Comments(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, ForeignKey('users.id'))
    author = relationship('Users', back_populates='comments')
    blog_id = db.Column(db.Integer, ForeignKey('blog_post.id'))
    blog = relationship('BlogPost', back_populates='comments')
