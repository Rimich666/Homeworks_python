from flask import (
    request
)
import json
import datetime
from . import api_app
from ..models import (
    Order
)


@api_app.route('/orders/', methods=['GET', 'POST'], endpoint='orders')
def api_orders():
    if request.method == 'GET':
        q = Order.query.filter_by(guid=None).all()
        orders = [{'id': order.id,
                   'num': order.num,
                   'guid': order.guid,
                   'date': order.date.isoformat(),
                   'sum': str(order.sum),
                   'buyer': order.buyer.kode,
                   'user': order.user.username,
                   'shop': order.shop.kode,
                   'products': [{'product': prod.product.kode,
                                 'quantity': str(prod.quantity),
                                 'price': str(prod.price),
                                 'sum': str(prod.sum)} for prod in order.orders_products]}
                  for order in q]
        return json.dumps(orders)
        pass
