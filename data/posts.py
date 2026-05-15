import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Post(SqlAlchemyBase):
    __tablename__ = 'posts'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    reply_to = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    image = sqlalchemy.Column(sqlalchemy.BLOB, nullable=True)
    file = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.Integer, default=datetime.datetime.now)

    board_on = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey('boards.name'))
    board = orm.relationship('Board')

    created_by = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey('users.name'))
    user = orm.relationship('User')
