from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
word = Table('word', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('word', String(length=140)),
    Column('translated', String(length=140)),
    Column('example', String(length=140)),
    Column('example_cn', String(length=140)),
    Column('wordbook_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['word'].columns['example'].create()
    post_meta.tables['word'].columns['example_cn'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['word'].columns['example'].drop()
    post_meta.tables['word'].columns['example_cn'].drop()
