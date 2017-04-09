from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
user = Table('user', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('email', VARCHAR(length=120)),
    Column('role', SMALLINT),
    Column('password', VARCHAR(length=120)),
    Column('username', VARCHAR(length=64)),
    Column('last_seen', DATETIME),
    Column('nickname', VARCHAR(length=64)),
    Column('user_info', VARCHAR(length=140)),
    Column('choice_words_table', VARCHAR(length=64)),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('username', String(length=64)),
    Column('nickname', String(length=64)),
    Column('email', String(length=120)),
    Column('password', String(length=120)),
    Column('role', SmallInteger, default=ColumnDefault(0)),
    Column('user_info', String(length=140)),
    Column('last_seen', DateTime),
    Column('choice_wordbook', String(length=64)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['user'].columns['choice_words_table'].drop()
    post_meta.tables['user'].columns['choice_wordbook'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['user'].columns['choice_words_table'].create()
    post_meta.tables['user'].columns['choice_wordbook'].drop()
