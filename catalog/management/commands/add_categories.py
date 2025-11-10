import os

from django.core.management import call_command
from django.core.management.base import BaseCommand

from catalog.models import Category


class Command(BaseCommand):
    help = "Кастомная команда для импорта данных Category из файла фикстуры."

    def handle(self, *args, **kwargs):
        # По заданию ДЗ, перед тем как создать выполняю удаление существующих записей
        Category.objects.all().delete()
        # Создаю путь до фикстуры
        fixture_file = os.path.join("data/fixtures", "categories_fixture.json")
        call_command("loaddata", fixture_file)
        self.stdout.write(self.style.SUCCESS("Успешный импорт данных из фикстуры."))
