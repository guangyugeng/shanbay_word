from app import app, db
from flask import render_template, flash, session, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required
from flask import g, Blueprint
from datetime import datetime
from app.models import Wordbook, Word, TodayWord, TodayWordbook, User, ROLE_USER, ROLE_ADMIN
from app.views.api import update_today_words

main = Blueprint('word', __name__)


@main.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        g.user.save()


@main.route('/word')
@login_required
def word():
    user = g.user

    return render_template('word/word.html',
        user = user
        )


@login_required
@main.route('/wordbook')
def wordbook():
    user = g.user
    learning_wordbook = user.learning_wordbook
    my_wordbooks = Wordbook.query.filter_by(user_id=user.id).all()

    return render_template('word/wordbook.html',
        user = user,
        learning_wordbook = learning_wordbook,
        my_wordbooks = my_wordbooks
                           )


@main.route('/setting')
@login_required
def setting():
    user = g.user
    today_words_amount = str(user.today_words_amount)
    learning_wordbook = user.learning_wordbook
    amounts = ['20', '50', '100', '150', '200', '250', '300', '400', '500', '600', '700']

    return render_template('word/setting.html',
        title = 'Home',
        user = user,
        today_words_amount = today_words_amount,
        learning_wordbook = learning_wordbook,
        amounts = amounts
                           )


@main.route('/new_word')
@login_required
def new_word():
    user = g.user
    wordbook = Wordbook.query.filter_by(book_name=user.learning_wordbook,user_id=user.id).first()
    words = Word.query.filter_by(wordbook_id=wordbook.id,learned=False).all()

    return render_template('word/new_word.html',
        words = words
                           )


@main.route('/today_word')
@login_required
def today_word():
    user = g.user
    today_wordbook_id = update_today_words(user, 100)
    today_words = TodayWord.query.filter_by(today_wordbook_id=today_wordbook_id).all()

    return render_template('word/today_word.html',
        words = today_words
                           )


@main.route('/learned_word')
@login_required
def learned_word():
    user = g.user
    wordbook = Wordbook.query.filter_by(book_name=user.learning_wordbook,user_id=user.id).first()
    words = Word.query.filter_by(wordbook_id=wordbook.id,learned=True).all()

    return render_template('word/learned_word.html',
        words = words
                           )

