from django.conf import settings
from django.db import models

import users.models


class Category(models.Model):
    """Модель Category представляет категорию товаров в интернет-магазине."""
    category_name = models.CharField(max_length=100, verbose_name="Наименование категории", help_text="Введите название категории", unique=True, blank=False)
    description = models.TextField(verbose_name="Описание категории", help_text="Введите описание категории", blank=True)

    def __str__(self):
        """Метод определяет строковое представление объекта. Полезно для отображения объектов в админке/консоли."""
        return f"{self.category_name}"

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["category_name"]
        db_table = "catalog_categories"


class Product(models.Model):
    """Модель Product представляет товар в интернет-магазине."""
    product_name = models.CharField(max_length=100, unique=True, blank=False, verbose_name="Наименование товара", help_text="Введите название товара")
    description = models.TextField(blank=True, verbose_name="Описание товара", help_text="Введите описание товара")
    image = models.ImageField(upload_to="product_image/", blank=True, null=True, verbose_name="Фотография товара", help_text="Загрузите фото товара")
    category = models.ForeignKey(blank=True, verbose_name="Категория товара", to=Category, on_delete=models.CASCADE, related_name="products", help_text="Выберите категорию")
    price = models.FloatField(blank=False, null=False, verbose_name="Цена товара", help_text="Укажите цену товара")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False, null=False, blank=False, verbose_name="Признак публикации", help_text="Зафиксируйте факт публикации")
    owner = models.ForeignKey(
        null=True,  # Разрешаем пустые значения в БД
        blank=True,  # Разрешаем пустое поле в формах
        default=None,  # По умолчанию None
        # Динамически подставляю текущую user модель, чего не делает такой простой вариант как "to=users.models.UserCustomer".
        # Если мы когда-нибудь изменим AUTH_USER_MODEL в settings.py, модель Product автоматически обновится.
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Владелец товара",
        help_text="Пользователь, создавший этот товар"
    )

    def __str__(self):
        """Метод определяет строковое представление объекта. Полезно для отображения объектов в админке/консоли."""
        return f"{self.product_name}"

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["product_name"]
        db_table = "catalog_products"
        permissions = [
            ("can_change_product_publication", "Может управлять публикацией продукта (опубликовать / отменить)"),
        ]


class ContactsData(models.Model):
    """Модель ContactsData для хранения контактных данных интернет-магазина."""
    country = models.CharField(max_length=100, verbose_name="Страна", help_text="Введите страну регистрации магазина")
    tax_id = models.CharField(max_length=20, verbose_name="ИНН", help_text="Введите ИНН магазина")
    address = models.TextField(verbose_name="Адрес", help_text="Введите юридический адрес магазина")

    def __str__(self):
        """Метод определяет строковое представление объекта. Полезно для отображения объектов в админке/консоли."""
        return f"{self.country}, {self.address}"

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"
        ordering = ["country"]
        db_table = "catalog_contacts_data"


class Feedback(models.Model):
    """Модель Feedback для хранения информации с обратной связью на странице 'contacts.html'."""
    name = models.CharField(blank=False, max_length=100, verbose_name="Имя пользователя")
    phone = models.CharField(blank=False, max_length=15, verbose_name="Телефон пользователя")
    message = models.TextField(blank=False, verbose_name="Сообщение от пользователя")

    def __str__(self):
        """Метод определяет строковое представление объекта. Полезно для отображения объектов в админке/консоли."""
        return f"{self.name}, {self.phone}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ["phone"]
        db_table = "catalog_feedback"
