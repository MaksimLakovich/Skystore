import os

from django.core.management import call_command
from django.core.management.base import BaseCommand

from blog.models import Article


class Command(BaseCommand):
    help = "Кастомная команда для импорта данных Article из файла фикстуры."

    def handle(self, *args, **kwargs):
        # Для удобства тестирования буду предварительно очищать БД при записи статей из фикстуры
        Article.objects.all().delete()
        # Создаю путь до фикстуры
        fixture_file = os.path.join("data/fixtures", "articles_fixture.json")
        call_command("loaddata", fixture_file)
        self.stdout.write(self.style.SUCCESS("Успешный импорт данных из фикстуры."))
