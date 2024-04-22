from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_login import LoginManager
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor

db = SQLAlchemy()
login_manager = LoginManager()
bootstrap = Bootstrap5()
ckeditor = CKEditor()


def create_application():
    app = Flask(__name__)
    app.config.from_object(Config)

    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    db.init_app(app)
    bootstrap.init_app(app)
    ckeditor.init_app(app)

    from .models import Comments, Users, BlogPost

    from .routes import main
    app.register_blueprint(main)

    return app


if __name__ == '__main__':
    app = create_application()
    app.run()
