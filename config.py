# encoding: utf-8
import os

DEBUG = True

SECRET_KEY = '%!IQOkRBntYHX@OJo5jVWeC6'
# 默认的数据源
SQLALCHEMY_DATABASE_URI = 'mysql://mysql:123456@172.16.50.112/flask_demo'

SQLALCHEMY_TRACK_MODIFICATIONS = True

# GNUCASH
ACCOUNTS_LIST = [
    # (***GNUCASH ACCOUNT PATH***),
    '资产:流动资产:储蓄存款',
]
