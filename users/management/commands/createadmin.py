import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from dotenv import load_dotenv

# Загрузка переменных из .env-файла
load_dotenv()


class Command(BaseCommand):
    help = "Кастомная команда для создания Администратора."

    def handle(self, *args, **options):
        User = get_user_model()  # Получаем модель пользователя
        admin_email = os.getenv("ADMIN_EMAIL")  # Устанавливаю почту админа из .env
        admin_password = os.getenv("ADMIN_PASSWORD")  #  Устанавливаю пароль админа из .env

        if User.objects.filter(email=admin_email).exists():
            self.stdout.write(self.style.WARNING(f"Администратор с почтой {admin_email} уже существует."))
        else:
            user = User.objects.create_superuser(
                email=admin_email,
                password=admin_password,
                username="Admin",
                first_name="Admin",
                last_name="Admin",
            )
            self.stdout.write(self.style.SUCCESS(f"Успешно создан администратор с почтой {user.email}"))
