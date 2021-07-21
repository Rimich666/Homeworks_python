from django.core.management.base import BaseCommand
from ...functions import create_trial_data


class Command(BaseCommand):
    def handle(self, *args, **options):
        create_trial_data()
