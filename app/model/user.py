# -*- coding: utf-8 -*-

from sqlalchemy import Column
from sqlalchemy import String

from app.model import Base
from app.config import UUID_LEN


class User(Base):

    sid = Column(String(UUID_LEN), unique=True, nullable=False)
    username = Column(String(20), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(80), nullable=False)
    token = Column(String(255), nullable=False)

    def __repr__(self):
        return "<User(name='%s', email='%s', token='%s')>" % \
            (self.username, self.email, self.token)

    FIELDS = {
        'sid': str,
        'username': str,
        'email': str,
        'token': str
    }

    FIELDS.update(Base.FIELDS)
