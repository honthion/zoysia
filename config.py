# encoding: utf-8
import ConfigParser
import logging
import os
import sys

from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy

# 项目名
PROJECT_NAME = "zoysia"
# 日志
DEBUG = True
logging.debug("root")
handler = logging.FileHandler('flask.log', encoding='UTF-8')
handler.setLevel(logging.DEBUG)
handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s'))
# GNUCASH
INDEX_ACCOUNTS_SHOW = u'储蓄存款:流动资产:资产'
# 读取配置文件
conf = ConfigParser.ConfigParser()
sys_name = os.name
CONF_DIR = ''
if sys_name == 'nt':
    CONF_DIR = 'C://Users//user//Dropbox//properties//zoysia//settings.ini'
elif sys_name == 'posix':
    CONF_DIR = '/data/config/properties/zoysia/settings.ini'
conf.read(CONF_DIR)
db_user = conf.get('guncash', 'mysql_username')
db_password = conf.get('guncash', 'mysql_password')
db_host = conf.get('guncash', 'mysql_host')
db_name = conf.get('guncash', 'mysql_dbname')
guncash_db_url = "mysql://%s:%s@%s/%s?charset=utf8" % (db_user, db_password, db_host, db_name)
SECRET_KEY = conf.get('global', 'SECRET_KEY')
# 数据源
SQLALCHEMY_DATABASE_URI = 'mysql://mysql:123456@172.16.50.112/flask_demo'
SQLALCHEMY_TRACK_MODIFICATIONS = True
db = SQLAlchemy()
# 其他
auth = HTTPBasicAuth()
reload(sys)
sys.setdefaultencoding('utf-8')
