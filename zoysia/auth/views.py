# encoding: utf-8

import re

from flask import g, jsonify, make_response, Blueprint

from zoysia.models import *
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()
# 创建蓝图
api = Blueprint('auth', __name__, url_prefix='/zoysia/auth')


# 登陆
@api.route('/authorizations', methods=['POST'])
@auth.login_required
def get_auth_token():
    token = g.current_user.generate_auth_token()
    return jsonify({'code': 200, 'msg': "登录成功", 'token': token.decode('ascii'), 'name': g.current_user.name})


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


@auth.verify_password
def verify_password(name_or_token, password):
    if not name_or_token:
        return False
    name_or_token = re.sub(r'^"|"$', '', name_or_token)
    user = User.verify_auth_token(name_or_token)
    if not user:
        user = User.query.filter_by(name=name_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.current_user = user
    return True
