from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
word = Table('word', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('English_word', VARCHAR(length=140)),
    Column('Chinese_word', VARCHAR(length=140)),
    Column('wordbook_id', INTEGER),
)

word = Table('word', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('word', String(length=140)),
    Column('translated', String(length=140)),
    Column('wordbook_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['word'].columns['Chinese_word'].drop()
    pre_meta.tables['word'].columns['English_word'].drop()
    post_meta.tables['word'].columns['translated'].create()
    post_meta.tables['word'].columns['word'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['word'].columns['Chinese_word'].create()
    pre_meta.tables['word'].columns['English_word'].create()
    post_meta.tables['word'].columns['translated'].drop()
    post_meta.tables['word'].columns['word'].drop()
