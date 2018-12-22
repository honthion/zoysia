# encoding: utf-8

import json
import logging

from flask import g, jsonify, Blueprint
from zoysia.auth.views import *
from zoysia.models import *
from config import *
log = logging.getLogger(__name__)
app = Flask(__name__)
# 创建蓝图
api = Blueprint('user', __name__, url_prefix='/zoysia/user')


# 获取用户信息
@api.route('', methods=['GET'])
@auth.login_required
def get_user():
    ret = {'code': 200, 'msg': u"获取用户成功", 'type': "Organization", 'name': g.current_user.name}
    log.info("get_user res:%s" % json.dumps(ret).decode('unicode-escape'))
    return jsonify(ret)


# 添加用户
@api.route('', methods=['POST'])
@auth.login_required
def add_user():
    user = User(
        name='admin',
        password=User.hash_password_method('123456'),
        phone='18623001528',
        profess='',
        grade='',
        email='honthion@gmail.com',
        group='',
        power='',
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"status": True})
