from django.core.management.base import BaseCommand
from ...functions import delete_all


class Command(BaseCommand):
    def handle(self, *args, **options):
        delete_all()
        print('delete all')
