import logging
import os

from flask import Flask
from flask_cors import CORS
from werkzeug.utils import import_string

import config
from zoysia.my_utils.encoder_util import CustomJSONEncoder

logger = logging.getLogger(__name__)


def create_app():
    app = Flask(__name__)
    app.port = 5000
    app.debug = config.DEBUG
    app.config.from_object(config)
    app.json_encoder = CustomJSONEncoder
    CORS(app, resources=r'/*')
    db = config.db
    app.url_map.strict_slashes = False
    app.add_url_rule('/', 'home', home)

    register_blueprints(app)

    db.init_app(app)

    return app


def home():
    return dict(name='Flask REST API')


def register_blueprints(app):
    root_folder = 'zoysia'

    for dir_name in os.listdir(root_folder):
        module_name = root_folder + '.' + dir_name + '.views'
        module_path = os.path.join(root_folder, dir_name, 'views.py')

        if os.path.exists(module_path):
            module = import_string(module_name)
            obj = getattr(module, 'app', None)
            if obj:
                app.register_blueprint(obj)
