from flask import Flask
from blog_v3.models import Comments, Users, BlogPost
from blog_v3 import create_application, db

app = create_application()

with app.app_context():
    db.create_all()