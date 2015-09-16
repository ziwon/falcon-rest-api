# -*- coding: utf-8 -*-

from sqlalchemy import Column
from sqlalchemy import String, Integer

from app.model import Base
from app.config import UUID_LEN


class User(Base):
    user_id = Column(Integer, primary_key=True)
    sid = Column(String(UUID_LEN), nullable=False)
    username = Column(String(20), nullable=False)
    email = Column(String(320), unique=True, nullable=False)
    password = Column(String(80), nullable=False)
    token = Column(String(255), nullable=False)

    def __repr__(self):
        return "<User(name='%s', email='%s', token='%s')>" % \
            (self.username, self.email, self.token)

    @classmethod
    def get_id(cls):
        return User.user_id

    @classmethod
    def find_by_email(cls, session, email):
        return session.query(User).filter(User.email == email).one()

    FIELDS = {
        'sid': str,
        'username': str,
        'email': str,
        'token': str
    }

    FIELDS.update(Base.FIELDS)
