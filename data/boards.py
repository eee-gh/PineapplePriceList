import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Board(SqlAlchemyBase):
    __tablename__ = 'boards'

    name = sqlalchemy.Column(sqlalchemy.String, nullable=False, primary_key=True, unique=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    picture = sqlalchemy.Column(sqlalchemy.BLOB, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    created_by = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey('users.name'))
    user = orm.relationship('User')
