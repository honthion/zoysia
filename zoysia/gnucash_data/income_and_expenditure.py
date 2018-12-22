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
