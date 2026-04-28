import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    name = sqlalchemy.Column(sqlalchemy.String, nullable=False, primary_key=True, unique=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    picture = sqlalchemy.Column(sqlalchemy.BLOB, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    boards = orm.relationship('Board', back_populates='user')
