# -*- coding: utf-8 -*-

from app import log
from app.utils.auth import decrypt_token
from app.errors import UnauthorizedError


LOG = log.get_logger()


class AuthHandler(object):

    def process_request(self, req, res):
        LOG.debug("Authorization: %s", req.auth)
        if req.auth is not None:
            token = decrypt_token(req.auth)
            if token is None:
                raise UnauthorizedError('Invalid auth token: %s' % req.auth)
            else:
                req.context['auth_user'] = token.decode('utf-8')
        else:
            req.context['auth_user'] = None
