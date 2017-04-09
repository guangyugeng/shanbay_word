from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
wordbook = Table('wordbook', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('book_name', VARCHAR(length=140)),
)

word_book = Table('word_book', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('book_name', String(length=140)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['wordbook'].drop()
    post_meta.tables['word_book'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['wordbook'].create()
    post_meta.tables['word_book'].drop()
