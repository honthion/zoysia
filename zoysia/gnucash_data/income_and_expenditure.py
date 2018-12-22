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


# 获取单个
def get(id):
    item = RecordIncomeExpenditure.query.filter(RecordIncomeExpenditure.id == id).first()
    ret = [item.to_dict()]
    return EnumResponse.success({"ret": ret})


# 修改单个
def update(id, request):
    item = RecordIncomeExpenditure.query.filter(RecordIncomeExpenditure.id == id).first()
    if item:
        j_data = json.loads(request.data)
        record_content = j_data['record_content']
        if record_content:
            item.record_content = record_content
        if 'admin' in j_data and j_data['admin']:
            remark = j_data['remark']
            entry_account_status = j_data['entry_account_status']
            reviewer = g.current_user.name,
            reviewer_id = g.current_user.id,
            item.remark = remark
            item.entry_account_status = int(entry_account_status)
            item.reviewer = reviewer
            item.reviewer_id = reviewer_id
            item.entry_account_time = datetime.now()
        db.session.add(item)
        db.session.commit()
    return EnumResponse.success('')


# 删除单个
def delete(id):
    item = RecordIncomeExpenditure.query.filter(RecordIncomeExpenditure.id == id).first()
    if item:
        db.session.delete(item)
        db.session.commit()
    return EnumResponse.success('')
