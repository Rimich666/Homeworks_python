from django.core.management.base import BaseCommand
from ...functions import create_random_order
from ...models import Order


class Command(BaseCommand):
    def handle(self, *args, **options):
        order = create_random_order()
        if order in Order.objects.all():
            print(f"create order # {order.num} is successful")
