from django import forms
from django.core.exceptions import ValidationError

from config.config import FORBIDDEN_WORDS
from .models import Product


class ProductForm(forms.ModelForm):
    """Форма для добавления пользователем нового товара на странице add_your_product.html."""

    class Meta:
        model = Product
        # fields = ['product_name', 'description', 'price', 'image', 'category']
        fields = "__all__"
        widgets = {
            'product_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название вашего продукта (max: 100 символов)',
                'required': True,
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите описание вашего продукта',
                'required': True,
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Укажите стоимость вашего продукта',
                'required': True,
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
            'category': forms.Select(attrs={
                'class': 'form-control',
            }),
        }

    def __init__(self, *args, **kwargs):
        """Убираю 'help_text' для всех полей чтоб это не выводилось по умолчанию на html-странице."""
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.help_text = None

    def clean_product_name(self):
        """Валидация атрибута формы 'product_name', которая проверяет отсутствие запрещенных слов в данном поле."""
        product_name = self.cleaned_data.get('product_name')
        words_in_product_name = product_name.split(' ')
        for word in words_in_product_name:
            if word.lower() in FORBIDDEN_WORDS:
                raise ValidationError(f'Поле product_name.verbose_name не может содержать это слово')
        return product_name

    def clean_description(self):
        """Валидация атрибута формы 'description', которая проверяет отсутствие запрещенных слов в данном поле."""
        description = self.cleaned_data.get('description')
        words_in_description = description.split(' ')
        for word in words_in_description:
            if word.lower() in FORBIDDEN_WORDS:
                raise ValidationError(f'Поле description.verbose_name не может содержать это слово')
        return description


class ContactForm(forms.Form):
    """Форма для заполнения и отправки пользователем обратной связи на странице contacts.html."""
    name = forms.CharField(max_length=100, label="Имя", required=True)
    phone = forms.CharField(max_length=15, label="Телефон", required=True)
    message = forms.CharField(widget=forms.Textarea, label="Сообщение", required=True)
