from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Создает группу 'Модератор продуктов' и назначает ей права."

    def handle(self, *args, **kwargs):
        # Создаю или получаю, если уже есть, группу "Модератор продуктов":
        group, created = Group.objects.get_or_create(name="Модератор продуктов")
        # Получаю предустановленное право для удаления продукта и кастомное право на управление публикацией продуктов:
        can_change_publication = Permission.objects.get(codename="can_change_product_publication")
        can_delete_product = Permission.objects.get(codename="delete_product")
        # Добавляю права в нашу группу:
        group.permissions.add(can_change_publication, can_delete_product)

        if created:
            self.stdout.write(self.style.SUCCESS("Группа 'Модератор продуктов' создана и права добавлены!"))
        else:
            self.stdout.write(self.style.SUCCESS("Группа 'Модератор продуктов' уже существует, права обновлены!"))
