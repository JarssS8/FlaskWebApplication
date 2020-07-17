from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy import Table
from sqlalchemy.orm import relationship

from techtest.connector import BaseModel

_article_region_table = Table(
    'article_region',
    BaseModel.metadata,
    Column('article_id', Integer, ForeignKey('article.id')),
    Column('region_id', Integer, ForeignKey('region.id')),
)

# Relationship table between Article and Author
_article_author_table = Table(
    'article_author',
    BaseModel.metadata,
    Column('article_id', Integer, ForeignKey('article.id')),
    Column('author_id', Integer, ForeignKey('author.id'))
)


class Article(BaseModel):
    __tablename__ = 'article'

    id = Column(
        Integer,
        name='id',
        nullable=False,
        primary_key=True,
        autoincrement=True,
    )

    title = Column(
        Text,
        name='title'
    )

    content = Column(
        Text,
        name='content'
    )

    regions = relationship(
        'Region',
        secondary=_article_region_table,
    )

    # I use uselist because I want a One-To-One Relationship
    author = relationship(
        'Author',
        secondary=_article_author_table,
        uselist=False
    )
