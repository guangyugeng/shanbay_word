from flask import Flask
# from flask_wtf.csrf import CsrfProtect
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)


app.config.from_object('config')
db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'


from app.views.general import main as general
from app.views.api import main as api
from app.views.word import main as word
from app.views.user import main as user

app.register_blueprint(general)
app.register_blueprint(api)
app.register_blueprint(word)
app.register_blueprint(user)


# app.config.from_object('config')
# CsrfProtect(app)


if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('tmp/microblog.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('shanbay_word startup')

