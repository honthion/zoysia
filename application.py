# coding:utf-8
import logging
import os

from flask import Flask
from flask_cors import CORS
from werkzeug.utils import import_string

import config
from common.my_utils.encoder_util import CustomJSONEncoder

logger = logging.getLogger(__name__)

PROJECT_NAME = config.PROJECT_NAME


# 创建app
def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    app.json_encoder = CustomJSONEncoder
    CORS(app, resources=r'/*')
    db = config.db
    app.url_map.strict_slashes = False
    app.add_url_rule('/', PROJECT_NAME, home)

    register_blueprints(app)

    db.init_app(app)

    return app


def home():
    return dict(name='Flask REST API')


# 注册蓝图
def register_blueprints(app):
    root_folder = PROJECT_NAME
    for dir_name in os.listdir(root_folder):
        module_name = root_folder + '.' + dir_name + '.views'
        module_path = os.path.join(root_folder, dir_name, 'views.py')

        if os.path.exists(module_path):
            module = import_string(module_name)
            obj = getattr(module, 'api', None)
            if obj:
                app.register_blueprint(obj)
