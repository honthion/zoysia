# -*- coding: utf-8 -*-


# 响应枚举
class EnumResponse(object):
    def __init__(self, code, msg, result):
        self.code = code
        self.msg = msg
        self.result = result

    # 成功
    @staticmethod
    def success(result):
        return EnumResponse(200, 'success', result)

    # 失败
    @staticmethod
    def error(error_info, result):
        return EnumResponse(error_info[0], error_info[1], result)


request_error = [1000, '请求参数异常']
sql_error = [2000, '数据库异常']
