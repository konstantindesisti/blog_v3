import os
from dotenv import load_dotenv


class Config:
    load_dotenv()
    # ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    # DB_PATH = os.path.join(ROOT_DIR, 'blog_v3_database.db')
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DB_URI')

    CKEDITOR_PKG_TYPE = 'basic'
