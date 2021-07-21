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


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('select_db')
        pass
