from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError

from users.models import UserCustomer


class UserCustomerRegistrationForm(UserCreationForm):
    """Форма для регистрации пользователя на сайте магазина."""

    class Meta:
        model = UserCustomer
        fields = ("email", "password1", "password2")
        widgets = {
            "email": forms.EmailInput(attrs={"placeholder": "Введите email"}),
            "password1": forms.PasswordInput(attrs={"placeholder": "Введите пароль"}),
            "password2": forms.PasswordInput(attrs={"placeholder": "Введите пароль повторно"}),
        }

    def clean_email(self):
        """Переопределение clean_email() для явной проверки уникальности email.
        Функция clean_email() нужна, даже если email уже unique=True в модели как у нас потому что unique=True в
        модели выбрасывает ошибку на уровне БД, но не показывает ее в форме, а clean_email() помогает показать
        пользователю в форме, что такой email уже занят."""
        email = self.cleaned_data.get("email")
        if UserCustomer.objects.filter(email=email).exists():
            raise ValidationError("Этот email уже используется. Пожалуйста, выберите другой.")
        return email

    def __init__(self, *args, **kwargs):
        """Добавляю CSS-классы ко всем полям формы. Убираем 'help_text' для всех полей, чтоб это больше не выводилось
        по умолчанию на html-странице."""
        super().__init__(*args, **kwargs)

        # ШАГ 1: Убираю help_text из вывода на странице, так как help_text из model.py и дублирует то,
        # что и так уже автоматически создает class UserCustomer(AbstractUser).
        for field_name, field in self.fields.items():
            field.help_text = None
            # ШАГ 2: Добавляю класс "form-control" для всех полей.
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs["class"] = "form-control"
            # ШАГ 3: Добавляю placeholder вручную для наших полей формы регистрации.
            placeholders = {
                "email": "Введите email",
                "password1": "Введите пароль",
                "password2": "Введите пароль повторно",
            }
            if field_name in placeholders:
                field.widget.attrs["placeholder"] = placeholders[field_name]


class UserCustomerLoginForm(AuthenticationForm):
    """Форма для входа ранее зарегистрированного пользователя на сайт магазина."""

    def __init__(self, *args, **kwargs):
        """Заменяю username на email. Добавляю CSS-классы ко всем полям формы. Убираю 'help_text' для всех полей,
        чтоб это больше не выводилось по умолчанию на html-странице."""
        super().__init__(*args, **kwargs)

        # Django использует "username" как ключ, но у нас логин по email
        self.fields["username"].widget = forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Введите email"
        })
        self.fields["password"].widget = forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Введите пароль"
        })
        for field_name, field in self.fields.items():
            field.help_text = None
