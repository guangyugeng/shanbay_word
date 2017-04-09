from flask import render_template, flash, session, redirect, url_for,Blueprint,abort,request,g
from app.models import User, ROLE_USER, ROLE_ADMIN
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime


main = Blueprint('user', __name__)


@main.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        g.user.save()


@main.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username = username).first()
    if user == None:
        flash('User ' + username + ' not found.')
        return redirect(url_for('index'))
    learning_wordbook = user.learning_wordbook

    return render_template('user/user.html',
        user = user,
        learning_wordbook = learning_wordbook)



@main.route('/edit_user', methods=['GET', 'POST'])
@login_required
def edit_user():

    return render_template('user/edit_user.html')
