from flask import render_template, flash, session, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from flask import g, Blueprint
from datetime import datetime
from app import db, lm
from app.models import User, ROLE_USER, ROLE_ADMIN

main = Blueprint('general', __name__)


@main.route('/')
@main.route('/index', methods = ['GET', 'POST'])
def index():
    if g.user is None or\
    g.user.is_authenticated == False :
        return redirect(url_for('general.login_view'))
    else:
        return render_template('general/index.html')

@main.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        g.user.save()

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@main.route('/login_view', methods = ['GET', 'POST'])
def login_view():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('general.index'))
    else:
        return render_template('general/login.html',
        title = 'Sign In',
        )

@main.route('/register', methods = ['GET', 'POST'])
def register():
    return render_template('general/register.html',
                           title = 'Register',
                           )

@login_required
@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('general.login_view'))


@main.errorhandler(404)
def internal_error(error):
    return render_template('base/404.html'), 404

@main.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('base/500.html'), 500
#