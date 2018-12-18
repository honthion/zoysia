# encoding: utf-8

from flask import g, jsonify, Blueprint

from config import auth

# 创建蓝图
app = Blueprint('user', __name__, url_prefix='/zoysia/user')


# 获取用户信息
@app.route('', methods=['GET'])
@auth.login_required
def get_user():
    return jsonify({'code': 200, 'msg': "获取用户成功", 'type': "Organization", 'name': g.admin.name})
