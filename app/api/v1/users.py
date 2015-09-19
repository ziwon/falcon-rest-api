# -*- coding: utf-8 -*-

import re
import falcon

from sqlalchemy.orm.exc import NoResultFound
from cerberus import Validator, ValidationError

from app import log
from app.api.common import BaseResource
from app.utils.hooks import auth_required
from app.utils.auth import encrypt_token, hash_password, verify_password, uuid
from app.model import User
from app.errors import AppError, InvalidParameterError, UserNotExistsError, PasswordNotMatch

LOG = log.get_logger()


FIELDS = {
    'username': {
        'type': 'string',
        'required': True,
        'minlength': 4,
        'maxlength': 20
    },
    'email': {
        'type': 'string',
        'regex': '[a-zA-Z0-9._-]+@(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,4}',
        'required': True,
        'maxlength': 320
    },
    'password': {
        'type': 'string',
        'regex': '[0-9a-zA-Z]\w{3,14}',
        'required': True,
        'minlength': 8,
        'maxlength': 64
    },
    'info': {
        'type': 'dict',
        'required': False
    }
}


def validate_user_create(req, res, resource, params):
    schema = {
        'username': FIELDS['username'],
        'email': FIELDS['email'],
        'password': FIELDS['password'],
        'info': FIELDS['info']
    }

    v = Validator(schema)
    try:
        if not v.validate(req.context['data']):
            raise InvalidParameterError(v.errors)
    except ValidationError:
        raise InvalidParameterError('Invalid Request %s' % req.context)


class Collection(BaseResource):
    """
    Handle for endpoint: /v1/users
    """
    @falcon.before(validate_user_create)
    def on_post(self, req, res):
        session = req.context['session']
        user_req = req.context['data']
        if user_req:
            user = User()
            user.username = user_req['username']
            user.email = user_req['email']
            user.password = hash_password(user_req['password']).decode('utf-8')
            user.info = user_req['info'] if 'info' in user_req else None
            sid = uuid()
            user.sid = sid
            user.token = encrypt_token(sid).decode('utf-8')
            session.add(user)
            self.on_success(res, None)
        else:
            raise InvalidParameterError(req.context['data'])

    @falcon.before(auth_required)
    def on_get(self, req, res):
        session = req.context['session']
        user_dbs = session.query(User).all()
        if user_dbs:
            obj = [user.to_dict() for user in user_dbs]
            self.on_success(res, obj)
        else:
            raise AppError()

    @falcon.before(auth_required)
    def on_put(self, req, res):
        pass


class Item(BaseResource):
    """
    Handle for endpoint: /v1/users/{user_id}
    """
    @falcon.before(auth_required)
    def on_get(self, req, res, user_id):
        session = req.context['session']
        try:
            user_db = User.find_one(session, user_id)
            self.on_success(res, user_db.to_dict())
        except NoResultFound:
            raise UserNotExistsError('user id: %s' % user_id)


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
            user_db = User.find_by_email(session, email)
            if verify_password(password, user_db.password.encode('utf-8')):
                self.on_success(res, user_db.to_dict())
            else:
                raise PasswordNotMatch()

        except NoResultFound:
            raise UserNotExistsError('User email: %s' % email)

    @falcon.before(auth_required)
    def process_resetpw(self, req, res):
        pass
