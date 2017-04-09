from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
user = Table('user', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('username', VARCHAR(length=64)),
    Column('nickname', VARCHAR(length=64)),
    Column('email', VARCHAR(length=120)),
    Column('password', VARCHAR(length=120)),
    Column('role', SMALLINT),
    Column('user_info', VARCHAR(length=140)),
    Column('last_seen', DATETIME),
    Column('learning_wordbook', VARCHAR(length=64)),
)

word = Table('word', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('word', VARCHAR(length=140)),
    Column('translated', VARCHAR(length=140)),
    Column('example', VARCHAR(length=140)),
    Column('example_cn', VARCHAR(length=140)),
    Column('learned', BOOLEAN),
    Column('wordbook_id', INTEGER),
)

wordbook = Table('wordbook', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('book_name', VARCHAR(length=140)),
    Column('user_id', INTEGER),
)

notes = Table('notes', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('note', String(length=140)),
    Column('learner', String(length=140)),
    Column('created_time', String, default=ColumnDefault(0)),
    Column('word_id', Integer),
    Column('word', String(length=140)),
)

users = Table('users', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('username', String(length=64)),
    Column('nickname', String(length=64)),
    Column('email', String(length=120)),
    Column('password', String(length=120)),
    Column('role', SmallInteger, default=ColumnDefault(0)),
    Column('user_info', String(length=140)),
    Column('last_seen', DateTime),
    Column('learning_wordbook', String(length=64)),
)

wordbooks = Table('wordbooks', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('book_name', String(length=140)),
    Column('user_id', Integer),
)

words = Table('words', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('word', String(length=140)),
    Column('translated', String(length=140)),
    Column('example', String(length=140)),
    Column('example_cn', String(length=140)),
    Column('learned', Boolean),
    Column('wordbook_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['user'].drop()
    pre_meta.tables['word'].drop()
    pre_meta.tables['wordbook'].drop()
    post_meta.tables['notes'].create()
    post_meta.tables['users'].create()
    post_meta.tables['wordbooks'].create()
    post_meta.tables['words'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['user'].create()
    pre_meta.tables['word'].create()
    pre_meta.tables['wordbook'].create()
    post_meta.tables['notes'].drop()
    post_meta.tables['users'].drop()
    post_meta.tables['wordbooks'].drop()
    post_meta.tables['words'].drop()
