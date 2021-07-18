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

MODELS = (OrdersProduct, Order, Price, Product, Customer, Shop, PricesType, Buyer)

MANY_TO_MANY = (
    {'mod': Customer, 'field': 'shops'},
)


class Command(BaseCommand):
    def handle(self, *args, **options):
        for m2m in MANY_TO_MANY:
            for obj in m2m['mod'].objects.all():
                getattr(obj, m2m['field']).clear()
        for Model in MODELS:
            Model.objects.all().delete()

        print('delete all')