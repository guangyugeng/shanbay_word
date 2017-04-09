from flask import request, g, Blueprint

import json

from app import db
from app.models import User, Wordbook, Word, Note, TodayWordbook, TodayWord
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime


main = Blueprint('api', __name__)


def update_today_words(user, N=100):
    wordbook = Wordbook.query.filter_by(book_name=user.learning_wordbook,user_id=user.id).first()
    form = {
        'user_id': user.id,
        'wordbook_id': wordbook.id,
        'wordbook': wordbook.book_name
    }
    today_wordbook = TodayWordbook(form)

    if today_wordbook.valid(N):
        print('exist')
        print(len(TodayWordbook.query.filter_by(wordbook_id=wordbook.id,user_id=user.id).all()))
        db_today_wordbook = TodayWordbook.query.filter_by(wordbook_id=wordbook.id,user_id=user.id).first()
        db_today_wordbook_id = db_today_wordbook.id
        update_today_words_amount(db_today_wordbook, wordbook, N)
    else:
        db_today_wordbook_id = init_today_wordbook(today_wordbook, wordbook, user, N)

    return db_today_wordbook_id


def update_today_words_amount(today_wordbook, wordbook, N):
    learned_today_words = TodayWord.query.filter_by(today_wordbook_id=today_wordbook.id,learned=True).all()
    unlearned_today_words = TodayWord.query.filter_by(today_wordbook_id=today_wordbook.id,learned=False).all()
    old_amount = len(learned_today_words) + len(unlearned_today_words)
    if old_amount == N:
        pass
    elif old_amount > N:
        count = old_amount - N
        if unlearned_today_words is not None:
            for w in unlearned_today_words:
                w.delete()
                count -= 1
                if count == 0:
                    break

        if count > 0:
            for w in learned_today_words:
                w.delete()
                count -= 1
                if count == 0:
                    break
    else:
        unknown_words = Word.query.filter_by(wordbook_id=wordbook.id,learned=False).all()
        count = 0
        for w in unknown_words:
            wf = {
                'word':w.word,
                'translated':w.translated,
                'example':w.example,
                'example_cn':w.example_cn
            }
            today_word = TodayWord(wf, today_wordbook.id)
            print(today_word)
            today_word.save()
            print(today_word.today_wordbook_id,today_wordbook.id)
            count += 1
            if count == N - old_amount:
                break


def init_today_wordbook(today_wordbook, wordbook, user, N):
    today_wordbook.save()
    db_today_wordbook = TodayWordbook.query.filter_by(wordbook_id=wordbook.id,user_id=user.id).first()
    unknown_words = Word.query.filter_by(wordbook_id=wordbook.id,learned=False).all()
    count = 0
    for w in unknown_words:
        wf = {
            'word':w.word,
            'translated':w.translated,
            'example':w.example,
            'example_cn':w.example_cn
        }
        today_word = TodayWord(wf, db_today_wordbook.id)
        print(today_word)
        today_word.save()
        print(today_word.today_wordbook_id)
        count += 1
        if count == N:
            break
    user.today_wordbook_id = db_today_wordbook.id
    user.today_words_amount = N
    user.save()

    return db_today_wordbook.id


@main.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        g.user.save()


@main.route('/api/user/login', methods=['POST'])
def user_login():
    form = request.form

    # print(form)
    u = User(form)
    r = {
        'data': []
    }
    # u.save()
    print(u, u.exist())
    if u.exist():
        r['success'] = True
        db_u = User.query.filter_by(username=u.username).first()

        login_user(db_u)
        if db_u.learning_wordbook is not None:
            update_today_words(db_u, db_u.today_words_amount)
        print(db_u,db_u.id)

        # r['data'] = u.json()
    else:
        r['success'] = False
        message = u.error_message('login')
        r['message'] = message

    return json.dumps(r, ensure_ascii=False)


@main.route('/api/user/register', methods=['POST'])
def user_register():

    form = request.form
    u = User(form)
    r = {
        'data': []
    }
    print("1111")
    if u.valid():
        print(u.nickname)
        nickname = User.make_unique_nickname(form['nickname'])
        u.nickname = nickname
        u.save()
        r['success'] = True
        # r['data'] = u.json()
    else:
        r['success'] = False
        message = u.error_message('register')
        r['message'] = message

    return json.dumps(r, ensure_ascii=False)


@main.route('/api/user/edit', methods=['POST'])
@login_required
def user_edit():

    form = request.form
    u = g.user
    r = {
        'data': []
    }
    print("cunzal",u.valid())
    if not u.valid():
        r['success'] = True
        r['username'] = u.username
        # print(db_u,db_u.id)
        print(form['nickname'])
        g.user.nickname = User.make_unique_nickname(form['nickname'])
        print("11111")
        print(form['info'])
        print("11111")

        g.user.user_info = form['info']
        print("11111")

        g.user.save()

        print("11111")
        # print(db_u.nickname)

        db.session.commit()
    else:
        r['success'] = False
        message = u.error_message('edit')
        r['message'] = message

    return json.dumps(r, ensure_ascii=False)


@main.route('/api/wordbook/add', methods=['POST'])
def wordbook_add():
    print("add")
    form = request.form
    r = {
        'data': []
    }
    book_name = form['book_name']
    wordbook = Wordbook.query.filter_by(book_name=book_name,user_id=g.user.id).first()

    if wordbook is not None:
        r['success'] = False
        r['message'] = "单词书已存在"
        return json.dumps(r, ensure_ascii=False)
    else:
        wordbook = Wordbook(book_name, g.user.id)
        wordbook.save()

        # 此处硬编码
        with open('wordbook.json', 'r') as f:
            wordbook_data = json.loads(f.read())
            # print(wordbook_data)
            for w in wordbook_data:
                word = Word(w, wordbook.id)
                word.save()
                # print(word.word)
        r['success'] = True

    return json.dumps(r, ensure_ascii=False)


@main.route('/api/word/setting', methods=['POST'])
def word_setting():
    print("add")
    user = g.user
    form = request.form
    r = {
        'data': []
    }
    if form['quota'] is not None:
        user.today_words_amount= form['quota']
        user.save()
        update_today_words(user, user.today_words_amount)
        r['success'] = True

    else:
        # print(wb+"is existed.")
        r['success'] = False
        message = '未知错误'
        r['message'] = message

    return json.dumps(r, ensure_ascii=False)


@main.route('/api/wordbook/choice', methods=['POST'])
def wordbook_choice():
    print("add")
    form = request.form
    r = {
        'data': []
    }
    if form['book_name'] is not None:
        g.user.learning_wordbook = form['book_name']
        g.user.save()
        update_today_words(g.user)
        r['success'] = True

    else:
        # print(wb+"is existed.")
        r['success'] = False
        message = '请输入书名'
        r['message'] = message

    return json.dumps(r, ensure_ascii=False)


@main.route('/api/words/start_learn', methods=['GET'])
def words_start_learn():
    print("start")
    user = g.user

    r = {
        'data': []
    }
    # today_wordbook = TodayWordbook.query.filter_by(user_id=user.id).first()
    # print('sd',today_wordbook.user_id)
    # word = TodayWord.query.filter_by(today_wordbook_id=today_wordbook.id,learned=False).first()
    today_word = TodayWord.query.filter_by(today_wordbook_id=user.today_wordbook_id, learned=False).first()
    # today_words = TodayWord.query.filter_by(today_wordbook_id=user.today_wordbook_id).all()

    if user.learning_wordbook is None:
        r['success'] = False
        r['message'] = "请选择学习的单词书"
    elif today_word is None:
        r['success'] = False
        r['message'] = "今日单词已学完"
    else:
        r['success'] = True
        r['data'] = today_word.json()
        # print(wb+"is existed.")
    # if form['word'] is not None:
    #     learned_word = LearnedWord(form['word'],g.user.id)
    #     if learned_word.valid():
    #         learned_word.save()
    #         r['success'] = True
    #
    # else:
    #     # print(wb+"is existed.")
    #     r['success'] = False
    #     # message = wb.error_message('register')
        # r['message'] = message

    return json.dumps(r, ensure_ascii=False)


@main.route('/api/words/known', methods=['POST'])
def words_known():
    print("start")
    user = g.user
    form = request.form
    r = {
        'data': [],
        'data2': [],
        'data3': []
    }

    today_wordbook = TodayWordbook.query.filter_by(user_id=user.id).first()

    today_word = TodayWord.query.filter_by(today_wordbook_id=today_wordbook.id,learned=False).first()
    word = Word.query.filter_by(wordbook_id=today_wordbook.wordbook_id,word=today_word.word).first()

    today_word.known()
    # today_word.save()
    mine_notes = Note.query.filter_by(word_id=word.id,learner=g.user.username).all()
    user_notes = Note.query.filter_by(word=word.word).all()

    if word is not None:
        r['success'] = True
        r['data'] = word.json()
        if user_notes is not None:
            for user_note in user_notes:
                print(user_note.note)
                # note_dict = { }
                r['data2'].append(user_note.json())
            for mine_note in mine_notes:
                print(mine_note.note)
                # note_dict = { }
                r['data3'].append(mine_note.json())
            # json.dumps(r['data2'], ensure_ascii=False)
    else:
        # print(wb+"is existed.")
        r['success'] = False
        r['message'] = "今日单词已学完"

    return json.dumps(r, ensure_ascii=False)


@main.route('/api/words/unknown', methods=['POST'])
def words_unknown():
    print("start")
    user = g.user
    form = request.form
    r = {
        'data': [],
        'data2': [],
        'data3': []
    }
    today_wordbook = TodayWordbook.query.filter_by(user_id=user.id).first()
    today_word = TodayWord.query.filter_by(today_wordbook_id=today_wordbook.id,learned=False).first()
    today_word.learned = True
    today_word.save()

    word = Word.query.filter_by(wordbook_id=today_wordbook.wordbook_id,word=today_word.word).first()

    mine_notes = Note.query.filter_by(word_id=word.id,learner=user.username).all()
    print(mine_notes)
    user_notes = Note.query.filter_by(word=word.word).all()

    if word is not None:
        r['success'] = True
        r['data'] = word.json()
        if user_notes is not None:
            for user_note in user_notes:
                print(user_note.note,'1')
                # note_dict = { }
                r['data2'].append(user_note.json())
            for mine_note in mine_notes:
                print(mine_note.note,'2')
                # note_dict = { }
                r['data3'].append(mine_note.json())
            # json.dumps(r['data2'], ensure_ascii=False)
    else:
        # print(wb+"is existed.")
        r['success'] = False
        r['message'] = "今日单词已学完"

    print(r['data2'])
    return json.dumps(r, ensure_ascii=False)


@main.route('/api/words/detail', methods=['GET'])
def words_detail():
    print("start")
    user = g.user
    # form = request.form
    r = {
        'data': []
    }

    today_wordbook = TodayWordbook.query.filter_by(user_id=user.id).first()
    word = TodayWord.query.filter_by(today_wordbook_id=today_wordbook.id,learned=False).first()

    if word is not None:
        r['success'] = True
        r['data'] = word.json()
    else:
        # print(wb+"is existed.")
        r['success'] = False
        r['message'] = "今日单词已学完"

    return json.dumps(r, ensure_ascii=False)


@main.route('/api/note/add', methods=['POST'])
def note_add():
    print("start")
    user = g.user
    form = request.form
    r = {
        'data': []
    }
    print(form['word'])
    if form['note'] is not Note:
        wordbook = Wordbook.query.filter_by(book_name=user.learning_wordbook,user_id=user.id).first()
        word = Word.query.filter_by(wordbook_id=wordbook.id,learned=False,word=form['word']).first()

        note_form = {
            'note':form['note'],
            'word':word.word,
            'word_id':word.id,
            'learner':g.user.username
        }

        note = Note(note_form)
        note.save()
        # known_word.learned = True
        # known_word.save()
        # next_word = Word.query.filter_by(wordbook_id=wordbook.id,learned=False).first()

        r['success'] = True
        # r['data'].append(word.json())
        r['data'] = note.json()
    else:

        r['success'] = False
        message = '输入为空'
        r['message'] = message

    return json.dumps(r, ensure_ascii=False)


