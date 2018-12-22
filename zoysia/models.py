# encoding: utf-8

from config import db
from flask import Flask
from datetime import datetime
from passlib.apps import custom_app_context
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from flask import current_app


# 用户表
class User(db.Model):
    __tablename__ = 'sys_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ctime = db.Column(db.DateTime, default=datetime.now(), comment='创建时间')
    utime = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now(), comment='修改时间')
    name = db.Column(db.String(64), index=True, comment='姓名')
    password = db.Column(db.String(128), comment='密码')
    phone = db.Column(db.String(30), comment='电话号码')
    profess = db.Column(db.String(64))
    grade = db.Column(db.String(64), comment='性别')
    email = db.Column(db.String(120), index=True, comment='邮箱')
    group = db.Column(db.String(64))
    power = db.Column(db.Text(2000))

    def to_dict(self):
        columns = self.__table__.columns.keys()
        result = {}
        for key in columns:
            if key == 'pub_date':
                value = getattr(self, key).strftime("%Y-%m-%d %H:%M:%S")
            else:
                value = getattr(self, key)
            result[key] = value
        return result

    # 密码加密
    def hash_password(self, password):
        self.password = custom_app_context.encrypt(password)

    # 密码解析
    def verify_password(self, password):
        return custom_app_context.verify(password, self.password)

    # 获取token，有效时间10min
    def generate_auth_token(self, expiration=600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    # 密码加密
    @staticmethod
    def hash_password_method(password):
        return custom_app_context.encrypt(password)

    # 解析token，确认登录的用户身份
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data['id'])
        return user


# 进出账记录表
class RecordIncomeExpenditure(db.Model):
    __tablename__ = 'record_income_expenditure'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ctime = db.Column(db.DateTime, nullable=False, default=datetime.now(), comment='创建时间')
    utime = db.Column(db.DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now, comment='更新时间')
    creator_id = db.Column(db.Integer, nullable=False, comment='创建者用户Id')  # 用户id
    creator = db.Column(db.String(64), nullable=False, comment='创建者')  # 用户名
    record_content = db.Column(db.Text(2000), nullable=False, comment='内容（创建者添加）')  # 内容
    remark = db.Column(db.Text(2000), nullable=False, default='', comment='备注（审核者添加）')  # 备注
    entry_account_status = db.Column(db.Integer, nullable=False, default=0, comment='入账状态(0-未入账，1-已入账，2-记录作废)')
    entry_account_time = db.Column(db.DateTime, nullable=False, default=datetime.now(), comment='入账时间')
    reviewer_id = db.Column(db.Integer, nullable=False, default=0, comment='审核人Id')
    reviewer = db.Column(db.String(64), nullable=False, default='', comment='审核人')

    def to_dict(self):
        columns = self.__table__.columns.keys()
        result = {}
        for key in columns:
            if key in ['ctime', 'utime', 'entry_account_time']:
                value = getattr(self, key).strftime("%Y-%m-%d %H:%M:%S")
            else:
                value = getattr(self, key)
            result[key] = value
        return result
