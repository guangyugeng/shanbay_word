from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
today_words = Table('today_words', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('create_date', VARCHAR),
    Column('user_id', INTEGER),
    Column('wordbook_id', VARCHAR(length=64)),
)

today_wordbook = Table('today_wordbook', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('create_date', String, default=ColumnDefault(0)),
    Column('user_id', Integer),
    Column('wordbook_id', Integer),
    Column('wordbook', String(length=64)),
)

today_word = Table('today_word', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('word', VARCHAR(length=140)),
    Column('translated', VARCHAR(length=140)),
    Column('example', VARCHAR(length=140)),
    Column('example_cn', VARCHAR(length=140)),
    Column('today_words_id', INTEGER),
)

today_word = Table('today_word', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('word', String(length=140)),
    Column('translated', String(length=140)),
    Column('example', String(length=140)),
    Column('example_cn', String(length=140)),
    Column('learned', Boolean),
    Column('today_wordbook_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['today_words'].drop()
    post_meta.tables['today_wordbook'].create()
    pre_meta.tables['today_word'].columns['today_words_id'].drop()
    post_meta.tables['today_word'].columns['learned'].create()
    post_meta.tables['today_word'].columns['today_wordbook_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['today_words'].create()
    post_meta.tables['today_wordbook'].drop()
    pre_meta.tables['today_word'].columns['today_words_id'].create()
    post_meta.tables['today_word'].columns['learned'].drop()
    post_meta.tables['today_word'].columns['today_wordbook_id'].drop()
