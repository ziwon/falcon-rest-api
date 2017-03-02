# -*- coding: utf-8 -*-

import falcon
import sqlalchemy.orm.scoping as scoping
from sqlalchemy.exc import SQLAlchemyError

from app import log
from app import config
from app.errors import DatabaseError, ERR_DATABASE_ROLLBACK

LOG = log.get_logger()


class DatabaseSessionManager(object):
    def __init__(self, db_session):
        self._session_factory = db_session
        self._scoped = isinstance(db_session, scoping.ScopedSession)

    def process_request(self, req, res, resource=None):
        """
        Handle post-processing of the response (after routing).
        """
        req.context['session'] = self._session_factory

    def process_response(self, req, res, resource=None):
        """
        Handle post-processing of the response (after routing).
        """
        session = req.context['session']

        if config.DB_AUTOCOMMIT:
            try:
                session.commit()
            except SQLAlchemyError as ex:
                session.rollback()
                raise DatabaseError(ERR_DATABASE_ROLLBACK, ex.args, ex.params)

        if self._scoped:
            # remove any database-loaded state from all current objects
            # so that the next access of any attribute, or any query execution will retrieve new state
            session.remove()
        else:
            session.close()
