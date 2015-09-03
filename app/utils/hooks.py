# -*- coding: utf-8 -*-

import falcon


def auth_required(req, res, resource):
    if req.context['auth_user'] is None:
        raise falcon.HTTPUnauthorized('Unauthorized', "Authentication required")
