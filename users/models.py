from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class UserCustomer(AbstractUser):
    """Модель UserCustomer представляет пользователя магазина."""
    email = models.EmailField(unique=True, verbose_name="Email", help_text="Введите email")
    avatar = models.ImageField(upload_to="user_avatar", blank=True, null=True, verbose_name="Аватар пользователя", help_text="Загрузите аватар")
    phone_number = PhoneNumberField(blank=True, null=True, verbose_name="Телефон пользователя", help_text="Введите телефон")
    country = models.CharField(max_length=50, blank=True, null=True, verbose_name="Страна пользователя", help_text="Укажите страну")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username",]

    def __str__(self):
        """Метод определяет строковое представление объекта. Полезно для отображения объектов в админке/консоли."""
        return f"{self.email}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["email"]
