#encoding: utf-8
import os

DEBUG = True

SECRET_KEY = os.urandom(24)

SQLALCHEMY_DATABASE_URI = 'mysql://mysql:123456@172.16.50.112/flask_demo'
SQLALCHEMY_TRACK_MODIFICATIONS = True


