import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Post(SqlAlchemyBase):
    __tablename__ = 'posts'

    reply_to = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, unique=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    image = sqlalchemy.Column(sqlalchemy.BLOB, nullable=True)
    file = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    board_on = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey('boards.name'))
    board = orm.relationship('Board')

    created_by = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey('users.name'))
    user = orm.relationship('User')
