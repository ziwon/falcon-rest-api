# -*- coding: utf-8 -*-

import falcon
import json

from app import log
from app.utils.alchemy import  new_alchemy_encoder

LOG = log.get_logger()

CONTENT_TYPE_URL_ENCODED = 'application/x-www-form-urlencoded'
CONTENT_TYPE_JSON = 'application/json'


class BaseResource(object):

    def to_json(self, body_dict):
        LOG.info("dict=%s", body_dict)
        return json.dumps(body_dict)

    def from_db_to_json(self, db):
        return json.dumps(db, cls=new_alchemy_encoder())

    def abort(self, status=falcon.HTTP_500, message=None):
        raise falcon.HTTPError(status, message)

    def load_request(self, req, res):
        if req.content_length in (None, 0):
            return

        if req.content_type == CONTENT_TYPE_JSON:
            try:
                raw_json = req.stream.read()
            except Exception:
                self.abort(falcon.HTTP_500, 'Read Error')

            try:
                obj = json.loads(raw_json.decode('utf-8'))
            except (ValueError, UnicodeDecodeError):
                self.abort(falcon.HTTP_753, 'Malformed JSON')
            return obj
        elif req.content_type == CONTENT_TYPE_URL_ENCODED:
            return

    def on_get(self, req, res):
        res.status = falcon.HTTP_404

    def on_post(self, req, res):
        res.status = falcon.HTTP_404

    def on_put(self, req, res):
        res.status = falcon.HTTP_404

    def on_delete(self, req, res):
        res.status = falcon.HTTP_404
