# encoding: utf-8
from common.my_utils.response_enum import *
from zoysia.models import *
from flask import g, jsonify, make_response, Blueprint
import json


# 添加进出账信息
def add(request):
    j_data = json.loads(request.data)
    record_content = j_data['record_content']
    if not record_content:
        return EnumResponse.error(request_error, record_content)
    record = RecordIncomeExpenditure(creator=g.current_user.name,
                                     creator_id=g.current_user.id,
                                     record_content=record_content)
    db.session.add(record)
    db.session.commit()
    return EnumResponse.success("")


# 获取列表
def get_pages(request):
    page_num = request.args.get('page_num', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)
    query_string = request.args.get('query_string', '', type=str)
    id = request.args.get('id', 0, type=int)
    filters = {
        RecordIncomeExpenditure.record_content.like("%" + query_string + "%"),
    }
    if id:
        filters.add(RecordIncomeExpenditure.id == id)
    pagination = RecordIncomeExpenditure.query.filter(*filters).order_by(RecordIncomeExpenditure.utime.desc()).paginate(
        page=page_num,
        per_page=page_size,
        error_out=False)
    total_count = pagination.total
    ret = [item.to_dict() for item in pagination.items]
    return EnumResponse.success({"list": ret, "total_count": total_count})
