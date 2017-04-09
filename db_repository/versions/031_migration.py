from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
today_word = Table('today_word', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('word', String(length=140)),
    Column('translated', String(length=140)),
    Column('example', String(length=140)),
    Column('example_cn', String(length=140)),
    Column('today_words_id', Integer),
)

today_words = Table('today_words', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('create_date', String, default=ColumnDefault(0)),
    Column('user_id', Integer),
    Column('wordbook_id', String(length=64)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['today_word'].create()
    post_meta.tables['today_words'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['today_word'].drop()
    post_meta.tables['today_words'].drop()
