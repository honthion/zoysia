import errno
import hashlib
import io
import os
import psutil
import re
import shutil
import socket
from exts import db
from decimal import Decimal
from PIL import Image

from flask import current_app


class Book(db.Model):
    from_gnucash_api = True
    __bind_key__ = 'gnucash'
    __tablename__ = 'books'
    guid = db.Column(db.String(32), primary_key=True)
    root_account = db.Column(db.String(32), db.ForeignKey('Account.root_account'), db_column='root_account_guid')

    def __unicode__(self):
        return 'Root account: %s' % self.root_account


class Account(db.Model):
    from_gnucash_api = True
    __bind_key__ = 'gnucash'
    __tablename__ = 'accounts'
    guid = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(2048))
    parent_guid = db.Column(db.String(32), nullable=True)
    type = db.Column(db.String(2048), db_column='account_type')
    description = db.Column(db.String(2048))
    placeholder = db.Column(db.Boolean)

    _balances = {}
    _root = None
    _all_accounts = None
    _order = None

    def __unicode__(self):
        return self.path

    @staticmethod
    def from_path(path):
        parts = path.split(':')
        a = Account.get_root()
        if len(parts) > 0:
            for p in parts:
                found = False
                for c in a.children:
                    print c.name
                    print p
                    if c.name == p:
                        found = True
                        a = c
                        break
                if not found:
                    raise ValueError("Invalid account path '%s'" % path)
        return a

    @staticmethod
    def get_root():
        Account._ensure_cached()
        return Account._root

    @staticmethod
    def get(guid):
        Account._ensure_cached()
        return Account._all_accounts[guid]['account']

    @staticmethod
    def get_all():
        Account._ensure_cached()
        return [obj['account'] \
                for obj in Account._all_accounts.itervalues()]

    @staticmethod
    def _ensure_cached():
        if Account._root is None:
            Account._root = Book.objects.get().root_account

        if Account._all_accounts is None:
            def _path(account):
                if account.parent_guid is None:
                    return account.name
                parts = []
                a = account
                while not a.is_root:
                    parts.append(a.name)
                    a = Account.get(a.parent_guid)
                parts.reverse()
                return ':'.join(parts)

            Account._all_accounts = {}
            accounts = list(Account.objects.all())

            for a in accounts:
                Account._all_accounts[a.guid] = {
                    'account': a,
                    'path': '',
                    'children': [],
                }
            for a in accounts:
                Account._all_accounts[a.guid]['path'] = _path(a)
                if a.parent_guid is not None:
                    Account._all_accounts[a.parent_guid]['children'].append(a)
            for a in accounts:
                Account._all_accounts[a.guid]['children'] \
                    .sort(key=lambda a: a.name.lower())

        if Account._order is None:
            def _build_order(account):
                Account._order.append(account.guid)
                for a in account.children:
                    _build_order(a)

            Account._order = []
            _build_order(Account.get_root())

    @staticmethod
    def clear_caches():
        Account._balances = {}
        Account._root = None
        Account._all_accounts = None
        Account._order = None

    @property
    def description_or_name(self):
        if self.description:
            return self.description
        else:
            return self.name
    #
    # @property
    # def balance(self):
    #     if self.guid not in Account._balances:
    #         # return sum(s.amount() for s in self.split_set.all()) # SLOW
    #         cursor = connections['gnucash'].cursor()
    #         cursor.execute('''
    #       SELECT value_denom, SUM(value_num)
    #       FROM splits
    #       WHERE account_guid = %s
    #       GROUP BY value_denom
    #     ''', [self.guid])
    #         amount = Decimal(0)
    #         for row in cursor.fetchall():
    #             amount += row[1] / row[0]
    #         Account._balances[self.guid] = amount
    #     return Account._balances[self.guid]
    #
    # @property
    # def last_transaction_date(self):
    #     s = self.split_set.select_related(depth=1)
    #     utc = s.aggregate(max_date=Max('transaction__enter_date'))['max_date']
    #     return utc
    #
    # @property
    # def has_updates(self):
    #     return (Update.objects.filter(account_guid=self.guid).count() > 0)
    #
    # @property
    # def last_update(self):
    #     updates = Update.objects.filter(account_guid=self.guid)
    #     try:
    #         max_updated = updates.aggregate(max_updated=Max('updated'))['max_updated']
    #         return updates.filter(updated=max_updated).get()
    #     except:
    #         return None
    #
    # @property
    # def children(self):
    #     Account._ensure_cached()
    #     return list(Account._all_accounts[self.guid]['children'])
    #
    # @property
    # def is_root(self):
    #     return self.guid == Account.get_root().guid
    #
    # @property
    # def path(self):
    #     Account._ensure_cached()
    #     return Account._all_accounts[self.guid]['path']
    #
    # @property
    # def webapp_key(self):
    #     try:
    #         return unicode(current_app.config['SECRET_KEY'].ACCOUNTS_LIST.index(self.path))
    #     except ValueError:
    #         return self.guid
