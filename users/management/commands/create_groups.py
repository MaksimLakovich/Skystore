from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Создает группу 'Модератор продуктов' и назначает ей права."

    def handle(self, *args, **kwargs):
        # Создаю или получаю, если уже есть, группу "Модератор продуктов"
        group, created = Group.objects.get_or_create(name="Модератор продуктов")
        can_change_publication = Permission.objects.get(codename="can_change_product_publication")  # Получаю права
        group.permissions.add(can_change_publication)  # Добавляю права в группу

        if created:
            self.stdout.write(self.style.SUCCESS("Группа 'Модератор продуктов' создана и права добавлены!"))
        else:
            self.stdout.write(self.style.SUCCESS("Группа 'Модератор продуктов' уже существует, права обновлены!"))
