__author__ = 'guangyugeng'

# u = User.query.filter_by(username='guanyu').first()
# print(u)
import sqlalchemy
import os

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
print(SQLALCHEMY_DATABASE_URI)
CSRF_ENABLED = True
SECRET_KEY = 'secret'

# keys for localhost. Change as appropriate.

RECAPTCHA_PUBLIC_KEY = '6LeYIbsSAAAAACRPIllxA7wvXjIE411PfdB2gt2J'
RECAPTCHA_PRIVATE_KEY = '6LeYIbsSAAAAAJezaIq3Ft_hSTo0YtyeFG-JgRtu'

engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
DBSession = sessionmaker(bind=engine)

session = DBSession()

user = session.query(User).filter(User.id=='5').one()