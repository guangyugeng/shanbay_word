from app import db
from hashlib import md5
import time

ROLE_USER = 0
ROLE_ADMIN = 1


class ModelHelper(object):
    def __repr__(self):
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} \n>\n'.format(classname, s)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class User(db.Model, ModelHelper):

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True)
    nickname = db.Column(db.String(64), unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    password = db.Column(db.String(120), index = True)
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    user_info= db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)
    wordbook = db.relationship('Wordbook', backref = 'learner', lazy = 'dynamic')
    learning_wordbook = db.Column(db.String(64))
    today_wordbook_id = db.Column(db.Integer)
    today_words_amount = db.Column(db.Integer, default = 100)

    def __init__(self, form):
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.nickname = form.get('nickname', '')
        print(form.get('nickname', ''))
        self.email = form.get('email', '')

    @staticmethod
    def make_unique_nickname(nickname):
        if User.query.filter_by(nickname = nickname).first() == None:
            return nickname
        version = 2
        while True:
            new_nickname = nickname + str(version)
            if User.query.filter_by(nickname = new_nickname).first() == None:
                break
            version += 1
            return new_nickname

    def error_message(self, m):
        if m == 'register':
            return "用户名已存在"
        elif m == 'login':
            return "用户名或密码不正确"
        elif m == 'edit':
            return  "用户名不存在"
        else:
            return "error_message wrong"

    def valid(self):
        user = User.query.filter_by(username=self.username).first()
        if user is None:
            return True
        else:
            return False

    def exist(self):
        user = User.query.filter_by(username=self.username).first()
        if user is not None and user.password == self.password:
            return True
        else:
            return False

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/' + md5(self.email.encode(encoding='UTF-8',errors='strict')).hexdigest()+ '?d=mm&s=' + str(size)

    def __repr__(self):
        return '<User %r>' % (self.username)


class Word(db.Model, ModelHelper):

    id = db.Column(db.Integer, primary_key = True)
    word = db.Column(db.String(140))
    translated = db.Column(db.String(140))
    example = db.Column(db.String(140))
    example_cn = db.Column(db.String(140))
    learned = db.Column(db.Boolean)
    wordbook_id = db.Column(db.Integer, db.ForeignKey('wordbook.id'))

    def __init__(self, form, wordbook_id):
        self.wordbook_id = wordbook_id
        self.word = form.get('word', '')
        self.translated = form.get('translated', '')
        if form.get('example', '') is not None:
            self.example = form.get('example', '')
            self.example_cn = form.get('example_cn', '')
        self.learned = False

    def __repr__(self):
        return self.word

    def json(self):
        d = dict(
            id=self.id,
            word=self.word,
            translated=self.translated,
            example=self.example,
            example_cn=self.example_cn,
        )
        return d

    def error_message(self, m):
        if m == 'word_learn':
            return "单词书已学完"
        elif m == 'login':
            return "用户名或密码不正确"
        elif m == 'edit':
            return  "用户名不存在"
        else:
            return "error_message wrong"


class Note(db.Model, ModelHelper):

    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.String(140))
    learner = db.Column(db.String(140))
    created_time = db.Column(db.String(), default=0)
    word_id = db.Column(db.Integer)
    word = db.Column(db.String(140))

    def __init__(self, form):
        format = '%Y/%m/%d %H:%M:%S'

        v = int(time.time()) + 3600 * 8
        valuegmt = time.gmtime(v)
        dt = time.strftime(format, valuegmt)
        self.note = form.get('note', '')
        self.learner = form.get('learner', '')
        self.word_id = form.get('word_id', '')
        self.word = form.get('word', '')
        self.created_time = dt

    def json(self):
        d = dict(
            id=self.id,
            word=self.word,
            note=self.note,
            learner=self.learner,
            word_id=self.word_id,
            created_time=self.created_time,
        )
        return d

    def __repr__(self):
        return '<note %r>' % (self.note)


class Wordbook(db.Model, ModelHelper):

    id = db.Column(db.Integer, primary_key = True)
    book_name = db.Column(db.String(140))
    words = db.relationship('Word', backref = 'wordbook', lazy = 'dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, book_name, user_id):
        self.book_name = book_name
        self.user_id = user_id

    def exist(self):
        wordbook = Wordbook.query.filter_by(book_name=self.book_name).first()
        if wordbook is not None:
            return True
        else:
            return False

    def error_message(self, m):
        if m == 'wordbook_update':
            return "单词表已存在"
        else:
            return "error_message wrong"

    def __repr__(self):
        return self.book_name


class TodayWordbook(db.Model, ModelHelper):

    id = db.Column(db.Integer, primary_key = True)
    create_date = db.Column(db.String(), default=0)
    words = db.relationship('TodayWord', backref = 'today_wordbook', lazy = 'dynamic')
    user_id = db.Column(db.Integer)
    wordbook_id = db.Column(db.Integer)
    wordbook = db.Column(db.String(64))

    def __init__(self, form):
        format = '%Y/%m/%d'
        v = int(time.time()) + 3600 * 8
        valuegmt = time.gmtime(v)
        dt = time.strftime(format, valuegmt)
        self.wordbook = form.get('wordbook', '')
        self.wordbook_id = form.get('wordbook_id', '')
        self.user_id = form.get('user_id', '')
        self.create_date = dt

    def valid(self, N):
        today_wordbook = TodayWordbook.query.filter_by(wordbook_id=self.wordbook_id,user_id=self.user_id).first()

        if today_wordbook is not None:
            print(today_wordbook.create_date)
            print("self",self.create_date)
            if today_wordbook.create_date == self.create_date:
                print("true")
                return True
            else:
                print("false")
                words = TodayWord.query.filter_by(today_wordbook_id=today_wordbook.id).all()
                for w in words:
                    # uw = TodayWord.query.filter_by(w).all()
                    w.delete()
                today_wordbook.delete()
                return False
        else:
            print("none")
            return False

    def error_message(self, m):
        if m == 'wordbook_update':
            return "单词表已存在"
        else:
            return "error_message wrong"

    def __repr__(self):
        return self.wordbook


class TodayWord(db.Model, ModelHelper):

    id = db.Column(db.Integer, primary_key = True)
    word = db.Column(db.String(140))
    translated = db.Column(db.String(140))
    example = db.Column(db.String(140))
    example_cn = db.Column(db.String(140))
    learned = db.Column(db.Boolean)
    today_wordbook_id = db.Column(db.Integer, db.ForeignKey('today_wordbook.id'))

    def __init__(self, form, today_wordbook_id):
        self.today_wordbook_id = today_wordbook_id
        self.word = form.get('word', '')
        self.translated = form.get('translated', '')
        if form.get('example', '') is not None:
            self.example = form.get('example', '')
            self.example_cn = form.get('example_cn', '')
        self.learned = False

    def __repr__(self):
        return self.word

    def known(self):
        today_wordbook = TodayWordbook.query.filter_by(id=self.today_wordbook_id).first()
        word = Word.query.filter_by(wordbook_id=today_wordbook.wordbook_id,word=self.word).first()
        word.learned = True
        self.learned = True
        word.save()
        self.save()

    def json(self):

        d = dict(
            id=self.id,
            word=self.word,
            translated=self.translated,
            example=self.example,
            example_cn=self.example_cn,
        )
        return d

    def error_message(self, m):
        if m == 'word_learned':
            return "今日单词已学完"
        else:
            return "error_message wrong"

