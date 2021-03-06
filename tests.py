#!flask/bin/python
import os
import unittest

from config import basedir
from app import app, db
from app.models import User, Post
from datetime import datetime, timedelta

class TestCase(unittest.TestCase):
    form1 = {
        'nickname' : 'john',
        'email' : 'john@example.com',
        'username' : 'myname'
    }
    form2 = {
        'nickname' : 'susan',
        'email' : 'susan@example.com',
        'username' : 'susan'
    }
    form3 = {
        'nickname' : 'mary',
        'email' : 'mary@example.com',
        'username' : 'mary'
    }
    form4 = {
        'nickname' : 'david',
        'email' : 'david@example.com',
        'username' : 'david'
    }

    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        db.create_all()

    def tearDown(self):
        db.drop_all()

    def test_avatar(self):
        # create a user
        u = User(self.form1)
        avatar = u.avatar(128)
        expected = 'http://www.gravatar.com/avatar/d4c74594d841139328695756648b6bd6'
        assert avatar[0:len(expected)] == expected

    def test_make_unique_nickname(self):
        # create a user and write it to the database
        u = User(self.form1)
        db.session.add(u)
        db.session.commit()
        nickname = User.make_unique_nickname('john')
        assert nickname != 'john'
        # make another user with the new nickname
        nickname2 = User.make_unique_nickname('john')
        self.form1['nickname'] = nickname2
        self.form1['email'] = 'susan@example.com'
        self.form1['username'] = 'myname 2'
        # print('sds',nickname2,nickname)
        u = User(self.form1)
        db.session.add(u)
        db.session.commit()
        # nickname2 = User.make_unique_nickname('john')
        assert nickname2 != 'john'
        assert nickname2 == nickname

    # def test_follow(self):
    #     u1 = User(self.form1)
    #     u2 = User(self.form2)
    #     db.session.add(u1)
    #     db.session.add(u2)
    #     db.session.commit()
    #     assert u1.unfollow(u2) == None
    #     u = u1.follow(u2)
    #     db.session.add(u)
    #     db.session.commit()
    #     assert u1.follow(u2) == None
    #     assert u1.is_following(u2)
    #     assert u1.followed.count() == 1
    #     assert u1.followed.first().nickname == 'susan'
    #     assert u2.followers.count() == 1
    #     assert u2.followers.first().nickname == 'john'
    #     u = u1.unfollow(u2)
    #     assert u != None
    #     db.session.add(u)
    #     db.session.commit()
    #     assert u1.is_following(u2) == False
    #     assert u1.followed.count() == 0
    #     assert u2.followers.count() == 0
    #
    # def test_follow_posts(self):
    #     # make four users
    #     u1 = User(self.form1)
    #     u2 = User(self.form2)
    #     u3 = User(self.form3)
    #     u4 = User(self.form4)
    #     db.session.add(u1)
    #     db.session.add(u2)
    #     db.session.add(u3)
    #     db.session.add(u4)
    #     # make four posts
    #     utcnow = datetime.utcnow()
    #     p1 = Post(body = "post from john", author = u1, timestamp = utcnow + timedelta(seconds = 1))
    #     p2 = Post(body = "post from susan", author = u2, timestamp = utcnow + timedelta(seconds = 2))
    #     p3 = Post(body = "post from mary", author = u3, timestamp = utcnow + timedelta(seconds = 3))
    #     p4 = Post(body = "post from david", author = u4, timestamp = utcnow + timedelta(seconds = 4))
    #     db.session.add(p1)
    #     db.session.add(p2)
    #     db.session.add(p3)
    #     db.session.add(p4)
    #     db.session.commit()
    #     # setup the followers
    #     u1.follow(u1) # john follows himself
    #     u1.follow(u2) # john follows susan
    #     u1.follow(u4) # john follows david
    #     u2.follow(u2) # susan follows herself
    #     u2.follow(u3) # susan follows mary
    #     u3.follow(u3) # mary follows herself
    #     u3.follow(u4) # mary follows david
    #     u4.follow(u4) # david follows himself
    #     db.session.add(u1)
    #     db.session.add(u2)
    #     db.session.add(u3)
    #     db.session.add(u4)
    #     db.session.commit()
    #     # check the followed posts of each user
    #     f1 = u1.followed_posts().all()
    #     f2 = u2.followed_posts().all()
    #     f3 = u3.followed_posts().all()
    #     f4 = u4.followed_posts().all()
    #     assert len(f1) == 3
    #     assert len(f2) == 2
    #     assert len(f3) == 2
    #     assert len(f4) == 1
    #     assert f1 == [p4, p2, p1]
    #     assert f2 == [p3, p2]
    #     assert f3 == [p4, p3]
    #     assert f4 == [p4]

if __name__ == '__main__':
    unittest.main()