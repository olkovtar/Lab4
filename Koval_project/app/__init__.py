# -*- coding: UTF-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate
from flask_login import LoginManager
from config import config
from flask_recaptcha import ReCaptcha


db = SQLAlchemy()
login_manager = LoginManager()
# якщо є @login_required, то потім редіректить на account.login
# Фіксить помилку:
# werkzeug.routing.BuildError: Could not build url for endpoint 'login'. Did you mean 'account.login' instead?
login_manager.login_view = 'account.login'
login_manager.login_message = 'Please, sign in to access to the account'
login_manager.login_message_category = 'info'
migrate = Migrate()
recaptcha = ReCaptcha()


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config.get(config_name))
    recaptcha = ReCaptcha(app=app)

    app.config.update(dict(
        RECAPTCHA_ENABLED=True,
        RECAPTCHA_SITE_KEY="6Lf46dwoAAAAAIoiFrhbvSg9am9QITOsgp6V3Mkp",
        RECAPTCHA_SECRET_KEY="6Lf46dwoAAAAACg_SfCeNB6voAgL2dSVu79Coihb",
    ))

    recaptcha.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    login_manager.init_app(app)

    with app.app_context():

        from app.home import home_bp
        from app.account import account_bp

        app.register_blueprint(home_bp)
        app.register_blueprint(account_bp)

    return app
