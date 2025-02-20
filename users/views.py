import os

from django.contrib.auth import login
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from dotenv import load_dotenv

from users.forms import UserCustomerRegistrationForm

# Загрузка переменных из .env-файла
load_dotenv()


class RegisterView(FormView):
    """Представление для отображения страницы регистрации нового пользователя (register.html)."""

    form_class = UserCustomerRegistrationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("catalog:home_page")

    def form_valid(self, form):
        """Сохранение нового пользователя и автоматический вход после регистрации."""
        user = form.save()
        login(self.request, user)  # Автоматически входим в систему
        self.send_welcome_email(user.email)  # Запрос на отправку приветственного письма после регистрации
        return super().form_valid(form)

    def send_welcome_email(self, user):
        """Отправка приветственного письма пользователю после успешной регистрации."""
        subject = "Регистрация в магазине Skystore!"
        message = (
            f"Спасибо, что зарегистрировались в нашем магазине!\n\n"
            f"Почта для входа: {user.email}\n\n"
            f"После регистрации в интернет-магазине Skystore Вы можете публиковать свои плагины и"
            f"примеры кода для поиска покупателей."
        )
        from_email = os.getenv("YANDEX_EMAIL_HOST_USER")
        if not from_email:
            raise ValueError("Переменная окружения YANDEX_EMAIL_HOST_USER не загружена!")
        recipient_list = [user.email]
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=False,
        )
