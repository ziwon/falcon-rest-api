# -*- coding: utf-8 -*-

import os
import configparser
from itertools import chain


BRAND_NAME = 'Falcon REST API Template'

SECRET_KEY = 'xs4G5ZD9SwNME6nWRWrK_aq6Yb9H8VJpdwCzkTErFPw='
UUID_LEN = 10
UUID_ALPHABET = ''.join(map(chr, range(48, 58)))
TOKEN_EXPIRES = 3600

APP_ENV = os.environ.get('APP_ENV') or 'local'  # or 'live' to load live
INI_FILE = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        '../conf/{}.ini'.format(APP_ENV))

CONFIG = configparser.ConfigParser()
CONFIG.read(INI_FILE)
POSTGRES = CONFIG['postgres']
if APP_ENV == 'dev' or APP_ENV == 'live':
    DB_CONFIG = (POSTGRES['user'], POSTGRES['password'], POSTGRES['host'], POSTGRES['database'])
    DATABASE_URL = "postgresql+psycopg2://%s:%s@%s/%s" % DB_CONFIG
else:
    DB_CONFIG = (POSTGRES['host'], POSTGRES['database'])
    DATABASE_URL = "postgresql+psycopg2://%s/%s" % DB_CONFIG

DB_ECHO = True if CONFIG['database']['echo'] == 'yes' else False
DB_AUTOCOMMIT = True

LOG_LEVEL = CONFIG['logging']['level']
