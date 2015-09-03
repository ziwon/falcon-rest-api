# -*- coding: utf-8 -*-

import bcrypt
import shortuuid

from itsdangerous import TimestampSigner
from itsdangerous import SignatureExpired, BadSignature
from cryptography.fernet import Fernet, InvalidToken

from app.config import SECRET_KEY, TOKEN_EXPIRES, UUID_LEN, UUID_ALPHABET

app_secret_key = Fernet(SECRET_KEY)


def get_common_key():
    return app_secret_key


def uuid():
    return shortuuid.ShortUUID(alphabet=UUID_ALPHABET).random(UUID_LEN)


def encrypt_token(data):
        encryptor = get_common_key()
        return encryptor.encrypt(data.encode('utf-8'))


def decrypt_token(token):
    try:
        decryptor = get_common_key()
        return decryptor.decrypt(token.encode('utf-8'))
    except InvalidToken:
        return None


def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def verify_password(password, hashed):
    return bcrypt.hashpw(password.encode('utf-8'), hashed) == hashed


def generate_timed_token(user_dict, expiration=TOKEN_EXPIRES):
    s = TimestampSigner(SECRET_KEY, expires_in=expiration)
    return s.dumps(user_dict)


def verify_timed_token(token):
    s = TimestampSigner(SECRET_KEY)
    try:
        data = s.loads(token)
    except (SignatureExpired, BadSignature):
        return None
    return data
