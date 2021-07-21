from orders.models import (
    Buyer,
    Shop,
    PricesType,
    Price,
    Order,
    OrdersProduct,
    Product,
    Customer
)
import random
import datetime
from django.db import transaction
import json

MODELS = ({'obj': Buyer, 'key': 'buyers', 'f_key': 'buyer_id', 'f_name': 'buyer'},
          {'obj': PricesType, 'key': 'prices_type', 'f_key': 'pt_id', 'f_name': 'price_type'},
          {'obj': Shop, 'key': 'shops', 'f_key': 'shop_id', 'f_name': 'shop'},
          {'obj': Customer, 'key': 'users', 'f_key': 'user_id', 'f_name': 'customer'},
          {'obj': Product, 'key': 'products', 'f_key': 'product_id', 'f_name': 'product'},
          {'obj': Price, 'key': 'prices', 'f_key': False},
          {'obj': Order, 'key': 'orders', 'f_key': 'order_id', 'f_name': 'order'},
          {'obj': OrdersProduct, 'key': 'orders_products', 'f_key': False})

MANY_TO_MANY = (
    {'add_to': 'user_id',
     'added': 'shop_id',
     'table_key': 'territory',
     'field': 'shops'},
)

EXCEPT = ('id', 'role_id')

DEL_MODELS = (OrdersProduct, Order, Price, Product, Customer, Shop, PricesType, Buyer)

DEL_MANY_TO_MANY = (
    {'mod': Customer, 'field': 'shops'},
)


def create_trial_data():
    for_keys = {}
    with open("../dataJSON.json", "r", encoding='utf-8-sig') as read_file:
        data = json.load(read_file)
    for m in MODELS:
        Model = m['obj']
        if m['f_key']:
            for_keys[m['f_key']] = {}
        for row in data[m['key']]:
            model = Model()
            for kd in row.keys():
                fn = kd
                if kd in EXCEPT:
                    continue
                if kd.find('_id') > -1:
                    val = for_keys[kd][row[kd]]
                    fn = for_keys[kd]['field']
                else:
                    val = row[kd]
                setattr(model, fn, val)
            model.save()
            if m['f_key']:
                for_keys[m['f_key']][row['id']] = model
                for_keys[m['f_key']]['field'] = m['f_name']
    for m2m in MANY_TO_MANY:
        for rel in data[m2m['table_key']]:
            add_to = for_keys[m2m['add_to']][rel[m2m['add_to']]]
            added = for_keys[m2m['added']][rel[m2m['added']]]
            getattr(add_to, m2m['field']).add(added)
            add_to.save()


def delete_all():
    for m2m in DEL_MANY_TO_MANY:
        for obj in m2m['mod'].objects.all():
            getattr(obj, m2m['field']).clear()
    for Model in DEL_MODELS:
        Model.objects.all().delete()


def create_random_order():
    customer = random.choice(Customer.objects.all())
    if customer.username == 'admin':
        shops = Shop.objects.all()
    else:
        shops = customer.shops.all()
    products = Product.objects.all()
    shop = random.choice(shops)
    price_type = shop.price_type
    current_date = datetime.datetime.now(datetime.timezone.utc).astimezone()
    rows_count = random.randint(1, 10)
    order_sum = 0
    order = Order()
    order.buyer = shop.buyer
    order.date = current_date
    order.customer = customer
    order.shop = shop
    order.sum = 0
    with transaction.atomic():
        order.num = customer.number()
        customer.save()
        order.save()
        for _ in range(rows_count):
            product = random.choice(products)
            orders_product = OrdersProduct()
            orders_product.order = order
            orders_product.product = product
            orders_product.quantity = random.randint(1, 10)
            orders_product.price = Price.objects.filter(
                product=product, price_type=price_type, date__lte=current_date).order_by('date').last().price
            orders_product.sum = orders_product.quantity * orders_product.price
            order_sum += orders_product.sum
            orders_product.save()
        order.sum = order_sum
        order.save()
    return order
