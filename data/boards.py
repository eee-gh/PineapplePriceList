import sqlalchemy

from .db_session import SqlAlchemyBase


class Board(SqlAlchemyBase):
    __tablename__ = 'boards'

    name = sqlalchemy.Column(sqlalchemy.String, nullable=False, primary_key=True, unique=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
