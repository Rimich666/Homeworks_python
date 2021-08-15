from flask import Blueprint

orders_app = Blueprint("orders_app", __name__, url_prefix="/orders")

from . import orders
