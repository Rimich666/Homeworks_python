from flask import (
    redirect,
    url_for,
    render_template,
    request,
    make_response
)
from ..models import (
    Buyer,
    Shop,
    Order,
    Product,
    OrdersProduct,
    Price,
    CountOrder,
    db
)
from flask_login import current_user
from web_app.orders.forms import (
    AddOrderForm,
    Row
)
from web_app.orders import orders_app
from datetime import datetime
from decimal import Decimal
import json
from sqlalchemy.exc import IntegrityError
import sys


rows = {}


@orders_app.route('/', endpoint='orders')
def get_orders():
    rows.clear()
    orders = Order.query.filter_by(user=current_user).all()
    return render_template('orders/orders.html', orders=orders, user=current_user)
    pass


@orders_app.route('/<order_id>', endpoint='order')
def get_order(order_id):
    order = Order.query.filter_by(id=order_id).first()
    return render_template('orders/order.html', order=order)


def select_buyer(buyer_id):
    buyer = Buyer.query.filter_by(id=buyer_id).first()
    shops = filter(lambda shop: shop.buyer == buyer, current_user.shops)

    return {'buyer_id': buyer.id, 'buyer_name': buyer.buyer_name,
            'fragment': render_template('orders/shops.html', shops=shops)}


def select_shop(shop_id):
    shop = Shop.query.filter_by(id=shop_id).first()
    buyer = shop.buyer

    return {'buyer_id': buyer.id, 'buyer_name': buyer.buyer_name,
            'shop_id': shop.id, 'shop_name': shop.shop_name}
    pass


def select_product(quantity, product_id, shop_id):
    quant = Decimal(quantity)
    if product_id in rows.keys():
        rows[product_id].val = quant
        rows[product_id].sum = rows[product_id].val * rows[product_id].price_val
    else:
        type_price = Shop.query.filter_by(id=shop_id).first().prices_type
        date = datetime.now()

        prod = Product.query.filter_by(id=product_id).first()
        price = db.session.query(Price).filter(Price.pt_id == type_price.id, Price.product_id == prod.id,
                                               Price.date <= date).order_by(Price.date.desc()).first().price

        sum = quant * price
        id = "ord_prd_" + str(prod.id)
        rows[product_id] = Row(prd=prod, val=quant, prc=price, sum=sum, nm=id)

    return make_response('Я Вас услышал', 202)


def add_products():
    return render_template('orders/form.html', rows=rows.values(), len=len(rows))


def change_product(quantity, product_id):
    quant = Decimal(quantity)
    dict = {}
    rows[product_id].val = quant
    sum = rows[product_id].val * rows[product_id].price_val
    rows[product_id].sum = '{:,}'.format(sum).replace(',', ' ')
    if quant == 0:
        dict['render'] = True
        dict['fragment'] = delete_row(product_id)
    else:
        dict['render'] = False
        dict['quantity'] = str(quant)
        dict['sum'] = rows[product_id].sum
    return json.dumps(dict)
    pass


def delete_row(product_id):
    rows.pop(product_id)
    return render_template('orders/form.html', rows=rows.values(), len=len(rows))


workers = {'buyer_select': select_buyer,
           'shop_select': select_shop,
           'product_select': select_product,
           'render_products': add_products,
           'product_change': change_product,
           'delete_row': delete_row
           }


@orders_app.route('/new/', methods=['GET', 'POST'], endpoint='new')
def new_order():
    if request.method == 'GET':
        shops = current_user.shops
        buyers = [shop.buyer for shop in shops]
        products = Product.query.all()
        param = {'buyers': buyers,
                 'user': current_user,
                 'shops': shops,
                 'products': products}

        rows.clear()

        return render_template('orders/add.html', param=param)
    hd = request.headers
    content_type = hd.get('Content-Type')
    reason = hd.get('Reason', False)
    if content_type == 'application/json' and reason:
        return workers[reason](**request.json)
    return make_response(f"Content type: {content_type}", 200)


def db_session_commit():
    try:
        db.session.commit()
    except IntegrityError as ie:
        exc_type, value, traceback = sys.exc_info()
        val = str(value)
        if not (val.find('psycopg2.errors.UniqueViolation')
                and (val.find('orders_pkey') or val.find('orders_product_pkey'))):
            db.session.rollback()
            return {'commit': False, 'may': False, 'value': value}
        else:
            db.session.rollback()
            return {'commit': False, 'may': True}
        pass
    return {'commit': True}


@orders_app.route('/confirm/<buyer_id>/<shop_id>/', methods=['GET', 'POST'], endpoint='confirm')
def confirm_order(buyer_id, shop_id):
    buyer = Buyer.query.filter_by(id=buyer_id).first()
    shop = Shop.query.filter_by(id=shop_id).first()
    summa = sum([row.sum for row in rows.values()])
    param = {'user': current_user, 'buyer': buyer, 'shop': shop, 'rows': rows, 'sum': summa}
    form = AddOrderForm()
    if request.method == 'GET':
        return render_template('orders/confirm.html', form=form, param=param)
    if form.validate_on_submit():
        if current_user.count_order is None:
            count = CountOrder(current_user)
            db.session.add(count)
            db.session.commit()
        if len(rows) > 0:
            out = False
            while not out:
                order = Order()
                order.user = current_user
                order.buyer = buyer
                order.shop = shop
                order.date = datetime.now()
                order.num = current_user.count_order.number()
                order_sum = 0
                db.session.add(order)
                for row in rows.values():
                    order_product = OrdersProduct()
                    order_product.order = order
                    order_product.product = row.prod
                    order_product.quantity = row.val
                    order_product.price = row.price_val
                    order_product.sum = row.sum
                    order_sum += row.sum
                    db.session.add(order_product)
                order.sum = order_sum
                res = db_session_commit()
                if res['commit']:
                    out = True
                else:
                    if not res['may']:
                        return f"Чё то пошло не так <br>value: {res['value']}"
                pass
            rows.clear()
    return redirect(url_for('orders_app.orders'))
    pass
