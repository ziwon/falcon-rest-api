# -*- coding: utf-8 -*-

from __future__ import absolute_import

from sqlalchemy import Column
from sqlalchemy import DateTime, func
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.exc import SQLAlchemyError

from app import log
from app.utils import alchemy
from app.errors import DatabaseError, ERR_UNKNOWN

LOG = log.get_logger()


class BaseModel(object):
    created = Column(DateTime, default=func.now())
    modified = Column(DateTime, default=func.now(), onupdate=func.now())

    @declared_attr
    def __tablename__(self):
        return self.__name__.lower()

    @classmethod
    def fields(cls):
        l = []
        for k in cls.FIELDS.keys():
            l.append(cls.__dict__[k])
        return l

    @classmethod
    def find_one(cls, session, id):
        try:
            return session.query(cls).filter(cls.get_id() == id).one()
        except SQLAlchemyError as ex:
            raise DatabaseError(ERR_UNKNOWN, ex.args)

    @classmethod
    def find_update(cls, session, id, args):
        return session.query(cls).filter(cls.get_id() == id).update(args, synchronize_session=False)

    @classmethod
    def get_id(cls):
        pass

    def to_dict(self):
        intersection = set(self.__table__.columns.keys()) & set(self.FIELDS)
        return dict(map(
            lambda key:
                (key, 
                    (lambda value: self.FIELDS[key](value) if value else None)(getattr(self, key))), 
                intersection))

    FIELDS = {
        'created': alchemy.datetime_to_timestamp,
        'modified': alchemy.datetime_to_timestamp,
    }

Base = declarative_base(cls=BaseModel)
