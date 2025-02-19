import os

from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Кастомная команда для экспорта данных Category в файл фикстуры."

    def handle(self, *args, **kwargs):
        # Указываю путь для сохранения фикстуры
        fixture_file = os.path.join("data/fixtures", "categories_fixture.json")

        # Создаю директорию, если её ещё нет
        os.makedirs(os.path.dirname(fixture_file), exist_ok=True)

        # Вызываю dumpdata и формирую фикстуру
        with open(fixture_file, "w", encoding="utf-8") as file:
            call_command("dumpdata", "catalog.Category", stdout=file, indent=4)

        self.stdout.write(self.style.SUCCESS(f"Успешный экспорт данных в {fixture_file}"))
