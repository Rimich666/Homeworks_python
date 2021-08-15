from flask import (
    Blueprint,
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
    db
)
from flask_login import current_user
from ..forms.orders_forms import (
    AddOrderForm,
    Row,
    ProdField
)
from datetime import datetime
from decimal import Decimal

orders_app = Blueprint("orders_app", __name__, url_prefix="/orders")

#current_order_form: AddOrderForm
rows = {}


@orders_app.route('/', endpoint='orders')
def get_orders():
    orders = Order.query.filter_by(user=current_user).all()
    return render_template('orders/orders.html', orders=orders, user=current_user)
    pass


@orders_app.route('/<order_id>', endpoint='order')
def get_order(order_id):
    order = Order.query.filter_by(id=order_id).first()
    return render_template('orders/order.html', order=order)


def clear_list():
    for row in rows.values():
        delattr(AddOrderForm, row.name)
    rows.clear()


@orders_app.route('/new/<buyer_id>/<shop_id>', methods=['GET', 'POST'], endpoint='add')
def new_order(buyer_id, shop_id):

    if request.method == 'GET':
        shops = current_user.shops
        buyers = [shop.buyer for shop in shops]
        param = {'buyers': buyers, 'user': current_user}

        if int(buyer_id) + int(shop_id) > 0:
            buyer = None
            if int(buyer_id) > 0:
                buyer = Buyer.query.filter_by(id=buyer_id).first()
                shops = filter(lambda shop: shop.buyer == buyer, shops)
            if int(shop_id) > 0:
                shop = Shop.query.filter_by(id=shop_id).first()
                buyer = shop.buyer
                param['shop'] = shop
            param['buyer'] = buyer

        param['shops'] = shops
        if int(buyer_id) > 0 and int(shop_id) > 0:
            products = Product.query.all()
            param['products'] = products
        else:
            clear_list()
        form = AddOrderForm()
        return render_template('orders/add.html', form=form, param=param, rows=rows.values())
    return make_response('Постучался POST', 200)


@orders_app.route('/new_product/<shop_id>/<product_id>/<quantity>', endpoint='new_product')
def new_product(shop_id, product_id, quantity):
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

        prod_field = ProdField(id)
        setattr(AddOrderForm, id, prod_field)
    return make_response('Я Вас услышал', 200)
    pass
