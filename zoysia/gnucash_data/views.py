# coding:utf-8
from flask import (
    request
)

from zoysia.auth.views import *
from . import account
from . import income_and_expenditure as in_ex

# 创建蓝图
api = Blueprint('gnucash', __name__, url_prefix="/zoysia/gnucash")


# 获取当前储蓄金额
# 获取五大基本类型的当前balance
@api.route('/index', methods=['GET'])
@auth.login_required
def index():
    res = account.get_index_page_data()
    return jsonify({'code': 200,
                    'data': res,
                    'vision': {'name': "0.0.1", "body": {}},
                    'showing_index': True, })


# 获取tx 列表

@api.route('/<account_guid>/transactions', methods=['GET'])
@auth.login_required
def account_tx(account_guid):
    query_string = request.args.get('query_string', '')
    page_num = request.args.get('page_num', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)
    total_count, tx_list = account.get_guid_tx_list(guid=account_guid, query_string=query_string,
                                                    page_num=page_num, page_size=page_size)
    return jsonify({'code': 200,
                    'total_count': int(total_count),
                    'list': tx_list, })


# 获取子Account

@api.route('/<account_guid>/children', methods=['GET'])
@auth.login_required
def account_children(account_guid):
    ret = account.get_children(guid=account_guid)
    return jsonify({'code': 200,
                    'data': ret, })


# 添加进出账记录
@api.route('/income-expenditures', methods=['POST'])
@auth.login_required
def add_income_expenditure():
    ret = in_ex.add(request)
    return jsonify({"code": ret.code, "data": ret.result, "msg": ret.msg})


# 获取进出账记录
@api.route('/income-expenditures', methods=['GET'])
@auth.login_required
def get_income_expenditures():
    ret = in_ex.get_pages(request)
    return jsonify({"code": ret.code, "data": ret.result, "msg": ret.msg})


# 获取单个进出账记录
@api.route('/income-expenditure/<id>', methods=['GET'])
@auth.login_required
def get_income_expenditure(id):
    ret = in_ex.get(id)
    return jsonify({"code": ret.code, "data": ret.result, "msg": ret.msg})


# 修改单个进出账记录
@api.route('/income-expenditure/<id>', methods=['PUT'])
@auth.login_required
def update_income_expenditure(id):
    ret = in_ex.update(id, request)
    return jsonify({"code": ret.code, "data": ret.result, "msg": ret.msg})


# 删除单个进出账记录
@api.route('/income-expenditure/<id>', methods=['DELETE'])
@auth.login_required
def delete_income_expenditure(id):
    ret = in_ex.delete(id)
    return jsonify({"code": ret.code, "data": ret.result, "msg": ret.msg})
