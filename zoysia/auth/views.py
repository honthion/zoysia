# encoding: utf-8

import re

from flask import g, jsonify, make_response, session, Blueprint

from config import auth
from zoysia.auth.models import *

# 创建蓝图
app = Blueprint('auth', __name__, url_prefix='/zoysia')


# 登陆
@app.route('/authorizations', methods=['POST'])
@auth.login_required
def get_auth_token():
    token = g.admin.generate_auth_token()
    return jsonify({'code': 200, 'msg': "登录成功", 'token': token.decode('ascii'), 'name': g.admin.name})


# 登陆
@app.route('/login', methods=['POST'])
@auth.login_required
def get_auth_token_():
    token = g.admin.generate_auth_token()
    return jsonify({'code': 200, 'msg': "登录成功", 'token': token.decode('ascii'), 'name': g.admin.name})


# 获取用户信息
@app.route('/user', methods=['GET'])
@auth.login_required
def get_user():
    return jsonify({'code': 200, 'msg': "获取用户成功", 'type': "Organization", 'name': g.admin.name})


# 钩子函数(注销)
@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user': user}
    return {}


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


@auth.verify_password
def verify_password(name_or_token, password):
    if not name_or_token:
        return False
    name_or_token = re.sub(r'^"|"$', '', name_or_token)
    admin = Admin.verify_auth_token(name_or_token)
    if not admin:
        admin = Admin.query.filter_by(name=name_or_token).first()
        if not admin or not admin.verify_password(password):
            return False
    g.admin = admin
    return True
