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

    # my_wordbooks = ["CET-4","CET-6","TOEFL"]
    today_words_amount = str(user.today_words_amount)
    print(today_words_amount)
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

    print(words)
    # for v,w in words.item():
    #     print(w)
    return render_template('word/new_word.html',
        words = words)


@main.route('/today_word')
@login_required
def today_word():
    user = g.user
    today_wordbook_id = update_today_words(user, 100)
    # wordbook = Wordbook.query.filter_by(book_name=user.learning_wordbook,user_id=user.id).first()
    # form = {
    #     'user_id': user.id,
    #     'wordbook_id': wordbook.id
    # }
    # today_wordbook = TodayWordbook(form)
    # if today_wordbook.exist():
    #     print('exist')
    #     print(len(TodayWordbook.query.filter_by(wordbook_id=wordbook.id,user_id=user.id).all()))
    #     db_today_wordbook = TodayWordbook.query.filter_by(wordbook_id=wordbook.id,user_id=user.id).first()
    # else:
    #     today_wordbook.save()
    #     db_today_wordbook = TodayWordbook.query.filter_by(wordbook_id=wordbook.id,user_id=user.id).first()
    #
    #     unknown_words = Word.query.filter_by(wordbook_id=wordbook.id,learned=False).all()
    #     count = 0
    #     for w in unknown_words:
    #         wf = {
    #             'word':w.word,
    #             'translated':w.translated,
    #             'example':w.example,
    #             'example_cn':w.example_cn
    #         }
    #         today_word = TodayWord(wf, db_today_wordbook.id)
    #         print(today_word)
    #         today_word.save()
    #         print(today_word.today_wordbook_id)
    #         count += 1
    #         if count == 100:
    #             break
        # db_today_wordbook.save()

    # db_today_wordbook.delete()

    # print(today_wordbook.id,db_today_wordbook.id)
    # print(today_wordbook.wordbook_id,wordbook.id)
    # print(today_wordbook.user_id,user.id)
    # db_today_wordbook.delete()

    today_words = TodayWord.query.filter_by(today_wordbook_id=today_wordbook_id).all()
    # /
    # words = TodayWord.query.filter_by().all()
    # for w in words:
    #     # uw = TodayWord.query.filter_by(w).all()
    #     w.delete()

# user_id = db.Column(db.Integer)
#     wordbook_id
    # wordbook = [
    #     {
    #         'word': 'Beautiful',
    #         'translated': { 'adj': '漂亮' }
    #     },
    #     {
    #         'word': 'Apple',
    #         'translated': { 'n': '苹果' }
    #     }
    # ]
    # print(today_words)
    # for v,w in words.item():
    #     print(w)
    return render_template('word/today_word.html',
        words = today_words)


@main.route('/learned_word')
@login_required
def learned_word():
    user = g.user
    wordbook = Wordbook.query.filter_by(book_name=user.learning_wordbook,user_id=user.id).first()
    words = Word.query.filter_by(wordbook_id=wordbook.id,learned=True).all()


    print(words)
    # for v,w in words.item():
    #     print(w)
    return render_template('word/learned_word.html',
        words = words)

