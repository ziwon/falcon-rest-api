# -*- coding: utf-8 -*-

import falcon

from app import log
from app import config
from app.middleware import AuthHandler, DatabaseSessionManager
from app.database import session_factory, init_session
from app.api.v1 import users

LOG = log.get_logger()


class App(falcon.API):
    def __init__(self, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)
        LOG.info('API Server is starting')

        self.add_route('/v1/users', users.Collection())
        self.add_route('/v1/users/{user_id}', users.Item())

        self.add_route('/v1/users/self/login', users.Self())

init_session()
middleware = [AuthHandler(), DatabaseSessionManager(session_factory, config.DB_AUTOCOMMIT)]
application = App(middleware=middleware)


if __name__ == "__main__":
    from wsgiref import simple_server
    httpd = simple_server.make_server('127.0.0.1', 8000, application)
    httpd.serve_forever()
