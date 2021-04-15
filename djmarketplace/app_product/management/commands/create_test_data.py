from django.core.management.base import BaseCommand

from core.generate_test_data import create_test_warehouses


class Command(BaseCommand):
    help = f'Команда для создания тестовых данных'

    def handle(self, *args, **kwargs):
        create_test_warehouses()
