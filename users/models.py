from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField  # type: ignore
from users.managers import UserCustomerManager


class UserCustomer(AbstractUser):
    """Модель UserCustomer представляет пользователя магазина."""

    username = None
    email = models.EmailField(
        unique=True,
        verbose_name="Почта (username):",
        help_text="Введите email",
    )
    avatar = models.ImageField(
        upload_to="user_avatar",
        blank=True,
        null=True,
        verbose_name="Аватар:",
        help_text="Загрузите аватар",
    )
    phone_number = PhoneNumberField(
        blank=True,
        null=True,
        verbose_name="Телефон:",
        help_text="Введите телефон",
    )
    country = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Страна проживания:",
        help_text="Укажите страну",
    )
    first_name = models.CharField(
        max_length=30,
        blank=True,
        verbose_name="Имя:",
        help_text="Введите имя"
    )
    last_name = models.CharField(
        max_length=30,
        blank=True,
        verbose_name="Фамилия:",
        help_text="Введите фамилию"
    )

    objects = UserCustomerManager()  # Указываю кастомный менеджер для пользователя без поля username.

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        """Метод определяет строковое представление объекта. Полезно для отображения объектов в админке/консоли."""
        return f"{self.email}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["email"]
