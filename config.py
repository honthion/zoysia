# encoding: utf-8
import ConfigParser
import os
import sys
from logging.config import dictConfig


from flask_sqlalchemy import SQLAlchemy
# 项目名
PROJECT_NAME = "zoysia"
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

# 日志
DEBUG = True
dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': "[%(asctime)s] %(levelname)-8s [%(name)s:%(funcName)s:%(lineno)-3s:%(thread)d] %(message)s",
        }},
    'handlers': {
        'null': {
            'class': 'logging.NullHandler',
        },
        'logfile': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': conf.get('global', 'log_file_path'),
            'when': 'midnight',
            'interval': 1,
            'backupCount': 100,
            'formatter': 'default',
            'encoding': 'UTF-8'
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        }},
    'root': {
        'level': 'DEBUG',
        'handlers': ['console', 'logfile']},
    'loggers': {
        'flask': {
            'handlers': ['console'],
            'propagate': False,
            'level': 'WARN',
        },
    }
})

# 数据源
guncash_db_url = conf.get('guncash', 'mysql_url')
SECRET_KEY = conf.get('global', 'SECRET_KEY')
SQLALCHEMY_DATABASE_URI = conf.get('global', 'mysql_url')
SQLALCHEMY_TRACK_MODIFICATIONS = True
db = SQLAlchemy()
# 其他

reload(sys)
sys.setdefaultencoding('utf-8')


