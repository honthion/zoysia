# encoding: utf-8
import os
import ConfigParser

DEBUG = True

SECRET_KEY = '%!IQOkRBntYHX@OJo5jVWeC6'
# 默认的数据源
SQLALCHEMY_DATABASE_URI = 'mysql://mysql:123456@172.16.50.112/flask_demo'

SQLALCHEMY_TRACK_MODIFICATIONS = True

# GNUCASH
INDEX_ACCOUNTS_SHOW = u'储蓄存款:流动资产:资产'
ACCOUNTS_LIST = [
    u'储蓄存款:流动资产:资产',
]

conf = ConfigParser.ConfigParser()
sys = os.name
CONF_DIR = ''
if sys == 'nt':
    CONF_DIR = 'C://Users//user//Dropbox//properties//settings.ini'
elif sys == 'posix':
    CONF_DIR = '/data/config/properties/settings.ini'
conf.read(CONF_DIR)
db_user = conf.get('guncash', 'mysql_username')
db_password = conf.get('guncash', 'mysql_password')
db_host = conf.get('guncash', 'mysql_host')
db_name = conf.get('guncash', 'mysql_dbname')
guncash_db_url = "mysql://%s:%s@%s/%s?charset=utf8" % (db_user, db_password, db_host, db_name)
