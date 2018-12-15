# coding:utf-8
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging
import config
import copy
import json
from flask import Flask
from flask.ext.cache import Cache
import my_util

# 使用缓存
app = Flask(__name__)
# Check Configuring Flask-Cache section for more details
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# engine = create_engine("mysql://mysql:123456@172.16.50.112/gnucash?charset=utf8", echo=True)
engine = create_engine(config.guncash_db_url, echo=True)
db = engine.connect()


# 得到整个层级关系
@cache.cached(timeout=500, key_prefix='all_accounts')
def all_accounts():
    # 查出所有的account
    my_util.close_old_connections(db)
    ret_db = db.execute("""
        select  accounts.guid,accounts.name,accounts.account_type,accounts.parent_guid,accounts.commodity_guid  ,IFNULL(c1.sumx,0) sumx
        from gnucash.accounts  
        left JOIN (
        select s1.account_guid guid ,s1.sumx ,a.`name` from (
        select  account_guid,SUM(splits.quantity_num / splits.value_denom) sumx from gnucash.splits group by account_guid) s1
        left join gnucash.accounts a on s1.account_guid = a.guid) c1  on c1.guid=accounts.guid
    """)
    rets = ret_db.fetchall()
    dic = {ret.guid: {"guid": ret.guid, "name": ret.name, "account_type": ret.account_type, "balance": float(ret.sumx),
                      "commodity_guid": ret.commodity_guid, "parent_guid": ret.parent_guid, "children": []} for ret in
           rets}
    ret_db.close()
    # 将account的层级关系实现
    for k in dic:
        path = k
        v = dic.get(k)
        # 添加parent
        path_name = v.get('name')
        parent = dic.get(v.get('parent_guid'))
        while parent:
            path += ":" + (parent.get('guid') and parent.get('guid') or "")
            path_name += ":" + (parent.get('name') and parent.get('name') or "")
            parent = dic.get(parent.get('parent_guid'))
        v['path'] = path
        v['path_name'] = path_name
        # 添加children
        parent = dic.get(v.get('parent_guid'))
        if parent:
            parent['children'].append(v)
    # 将子元素的金额汇总到父元素
    for k in dic:
        v = dic.get(k)
        balance = v['balance']
        for parent_guid in v['path'].split(':')[1:]:
            dic.get(parent_guid)['balance'] += balance
    return dic


class Tx:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
    def __init__(self, guid, enter_date, description, quantity_num, name_path, account_guid, name):
        self.name = name
        self.guid = guid
        self.enter_date = enter_date
        self.quantity_num = quantity_num
        self.description = description
        self.name_path = name_path
        self.account_guid = account_guid


# 查询guid的交易列表
#  61e9f96387044f19e6288d8f64892a9
def get_guid_tx_list(guid, query_string, page_num=1, page_size=10):
    my_util.close_old_connections(db)
    sql_str = """
            select  s3.* from (
            select s1.guid guid  ,s1.enter_date enter_date ,s1.description description ,splits.account_guid account_guid ,a1.name `name`,splits.quantity_num/splits.quantity_denom quantity_num
            from  (
            select transactions.guid,transactions.enter_date,transactions.description description
            from gnucash.splits
            LEFT JOIN gnucash.transactions on transactions.guid = splits.tx_guid
            WHERE splits.account_guid='%s' 
            ) s1 
            LEFT JOIN gnucash.splits  ON s1.guid = splits.tx_guid
            LEFT JOIN gnucash.accounts a1 on  a1.guid = splits.account_guid
            order by splits.quantity_num desc)s3
            WHERE CONCAT(description,`name`) like '%%%s%%'
            group BY guid
            order BY enter_date desc LIMIT %d,%d
       """ % (str(guid), str(query_string), int((page_num - 1) * page_size), int(page_size))
    ret_db = db.execute(sql_str)
    rets = ret_db.fetchall()
    all_accounts_dic = all_accounts()
    ret = [{"guid": ret.guid, "enter_date": ret.enter_date, "description": ret.description,
            "quantity_num": float(ret.quantity_num), "name_path": all_accounts_dic.get(ret.account_guid)['path_name'],
            "account_guid": ret.account_guid, "name": ret.name, "children": []} for ret in rets]
    # ret = [Tx(ret.guid, ret.enter_date, ret.description, float(ret.quantity_num),
    #           all_accounts_dic.get(ret.account_guid)['path_name'], ret.account_guid, ret.name) for ret in rets]
    ret_db = db.execute(
        """
            select count(0) from (
            select  s3.* from (
            select s1.guid guid  ,s1.enter_date enter_date ,s1.description description ,splits.account_guid account_guid ,a1.name `name`,splits.quantity_num/splits.quantity_denom quantity_num
            from  (
            select transactions.guid,transactions.enter_date,transactions.description description
            from gnucash.splits
            LEFT JOIN gnucash.transactions on transactions.guid = splits.tx_guid
            WHERE splits.account_guid='%s' 
            ) s1 
            LEFT JOIN gnucash.splits  ON s1.guid = splits.tx_guid
            LEFT JOIN gnucash.accounts a1 on  a1.guid = splits.account_guid
            order by splits.quantity_num desc)s3
            WHERE CONCAT(description,`name`) like '%%%s%%'
            group BY guid)a0
        """ % (str(guid), str(query_string)))
    total_count = ret_db.fetchone()[0]
    return total_count, ret


# 首页数据
def get_index_page_data():
    dic = all_accounts()
    arr_5 = [v for k, v in dic.items() if len(v['path'].split(':')) == 2]
    arr_target = [v for k, v in dic.items() if
                  (v['path_name'] and v['path_name']).find(config.INDEX_ACCOUNTS_SHOW) == 0]
    arr_target.extend(arr_5)
    ret = copy.deepcopy(arr_target)
    for i in ret:
        i['children'] = None
    return ret


# 子项
def get_children(guid):
    dic = all_accounts()
    child_list = dic.get(guid)['children']
    ret = copy.deepcopy(child_list)
    for i in ret:
        i['children'] = None
    return ret
