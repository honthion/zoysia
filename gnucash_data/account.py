# coding:utf-8
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql://mysql:123456@172.16.50.112/gnucash", encoding="utf-8", echo=True)
db = engine.connect()


def all_account_map():
    result_proxy = db.execute("""
        select s1.* ,a.`name` from (
        select  guid,SUM(splits.quantity_num) sumx from gnucash.splits group by account_guid) s1
        left join gnucash.accounts a on s1.guid = a.guid
    """)
    counts = result_proxy.fetchall()
    result_proxy.close(),
    dic = {c.guid: float(c.sumx) for c in counts}
    return dic
