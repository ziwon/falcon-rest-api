# -*- coding: utf-8 -*-

import re
import falcon

from sqlalchemy import or_
from sqlalchemy.orm.exc import NoResultFound

from app import log
from app.api.common import BaseResource
from app.utils.hooks import auth_required
from app.utils.auth import encrypt_token, hash_password, verify_password, uuid
from app.model import User

LOG = log.get_logger()


class Collection(BaseResource):
    """
    Handle for endpoint: /v1/users
    """
    def on_post(self, req, res):
        session = req.context['session']
        user_req = self.load_request(req, res)
        if user_req:
            user = User()
            user.username = user_req['username']
            user.email = user_req['email']
            user.password = hash_password(user_req['password']).decode('utf-8')
            sid = uuid()
            user.sid = sid
            user.token = encrypt_token(sid).decode('utf-8')
            session.add(user)

            res.status = falcon.HTTP_201
            res.body = self.to_json({
                'meta': {
                    'code': 201
                }
            })
        else:
            self.abort(falcon.HTTP_400, "Invalid Parameter")

    def on_get(self, req, res):
        session = req.context['session']
        user_dbs = session.query(User).all()
        if user_dbs:
            res.status = falcon.HTTP_200
            res.body = self.from_db_to_json([user.to_dict() for user in user_dbs])
        else:
            self.abort(falcon.HTTP_500, "Server error")

    @falcon.before(auth_required)
    def on_put(self, req, res):
        pass


class Item(BaseResource):
    """
    Handle for endpoint: /v1/users/{user_id|user_sid}
    """
    @falcon.before(auth_required)
    def on_get(self, req, res, user_id):
        session = req.context['session']
        try:
            user_db = session.query(User).filter(or_(User.id == int(user_id), User.sid == user_id)).one()
            res.status = falcon.HTTP_200
            res.body = self.to_json(user_db.to_dict())
        except NoResultFound:
            res.status = falcon.HTTP_404
            res.body = self.to_json({
                'message': 'user not found (id: %s)' % user_id
            })


class Self(BaseResource):
    """
    Handle for endpoint: /v1/users/self
    """
    LOGIN = 'login'
    RESETPW = 'resetpw'

    def on_get(self, req, res):
        cmd = re.split('\\W+', req.path)[-1:][0]
        if cmd == Self.LOGIN:
            self.process_login(req, res)
        elif cmd == Self.RESETPW:
            self.process_resetpw(req, res)

    def process_login(self, req, res):
        email = req.params['email']
        password = req.params['password']
        session = req.context['session']
        try:
            user_db = session.query(User).filter(User.email == email).one()
            if verify_password(password, user_db.password.encode('utf-8')):
                res.status = falcon.HTTP_200
                res.body = self.to_json(user_db.to_dict())
            else:
                res.status = falcon.HTTP_401
                res.body = self.to_json({
                    'message': 'password not match'
                })
        except NoResultFound:
            res.status = falcon.HTTP_404
            res.body = self.to_json({
                'message': 'user not exists'
            })

    @falcon.before(auth_required)
    def process_resetpw(self, req, res):
        pass
