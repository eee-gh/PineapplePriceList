import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    name = sqlalchemy.Column(sqlalchemy.String, nullable=False, primary_key=True, unique=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    picture = sqlalchemy.Column(sqlalchemy.BLOB, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    boards = orm.relationship('Board', back_populates='user')

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def get_id(self):
        return str(self.name)
