# coding:utf-8
from flask import Blueprint

gnucash = Blueprint("gnucash", __name__)

import zoysia.gnucash_data.views
