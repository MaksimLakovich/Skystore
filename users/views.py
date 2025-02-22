import os

from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from dotenv import load_dotenv

from users.forms import UserCustomerRegistrationForm, UserCustomerLoginForm

# Загрузка переменных из .env-файла
load_dotenv()


class CustomRegisterView(FormView):
    """Представление для отображения страницы регистрации нового пользователя (register.html)."""

    form_class = UserCustomerRegistrationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("catalog:home_page")  # Редирект после регистрации

    def form_valid(self, form):
        """Сохранение нового пользователя и автоматический вход после регистрации."""
        user = form.save()
        login(self.request, user)
        self.send_welcome_email(user)  # Запрос на отправку приветственного письма после регистрации
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


class CustomLoginView(LoginView):
    """Представление для входа пользователя (login.html)."""

    template_name = 'users/login.html'
    success_url = reverse_lazy("catalog:home_page")
    # Явно указываю кастомную форму для входа пользователя, без этого у меня почему-то не подтягиваются определенные в
    # форме UserCustomerLoginForm стили (наверное, потому что по умолчанию LoginView использует стандартную
    # форму Django → AuthenticationForm.)
    authentication_form = UserCustomerLoginForm

    def get_success_url(self):
        """Явно указываю редирект переопределяя метод, так как обычный вариант в виде "success_url = reverse_lazy(
        'catalog:home_page'" не работал. Django его игнорировал и отправлял на /accounts/profile/"""
        return reverse_lazy("catalog:home_page")

    def form_valid(self, form):
        """Автоматический вход пользователя после успешной аутентификации."""
        login(self.request, form.get_user())
        return super().form_valid(form)
