from django.core.management.base import BaseCommand
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


class Command(BaseCommand):
    def handle(self, *args, **options):
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
