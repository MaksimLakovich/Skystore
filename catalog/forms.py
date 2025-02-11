import re

from django import forms
from django.core.exceptions import ValidationError

from config.config import ALLOWED_IMAGE_FORMATS, FORBIDDEN_WORDS, MAX_IMAGE_SIZE
from .models import Product


class ProductForm(forms.ModelForm):
    """Форма для добавления пользователем нового товара на странице add_your_product.html."""

    class Meta:
        model = Product
        # fields = ['product_name', 'description', 'price', 'image', 'category']
        fields = "__all__"
        widgets = {
            'product_name': forms.TextInput(attrs={'placeholder': 'Введите название продукта (max: 100 символов)'}),
            'description': forms.Textarea(attrs={'placeholder': 'Введите описание продукта'}),
            'price': forms.NumberInput(attrs={'placeholder': 'Укажите стоимость продукта'}),
            'image': forms.ClearableFileInput(),
            'category': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        """Добавляем CSS-классы ко всем полям формы. Убираем 'help_text' для всех полей, чтоб это больше не выводилось
        по умолчанию на html-странице."""
        super().__init__(*args, **kwargs)

        # ШАГ 1: Убираю help_text из вывода на странице, так как help_text из model.py и дублирует то,
        # что и так уже автоматически создает forms.ModelForm.
        for field_name, field in self.fields.items():
            field.help_text = None
            # ШАГ 2: Добавляю класс "form-control" для всех полей, кроме чекбоксов:
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-control'
            # ШАГ 3: Добавляю класс "form-check-input" для чекбоксов, если появится:
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'

    def clean_product_name(self):
        """Валидация атрибута формы 'product_name', которая проверяет отсутствие запрещенных слов в данном поле."""
        product_name = self.cleaned_data.get('product_name', '')
        for word in FORBIDDEN_WORDS:
            # Регулярное выражение проверяет запрещенное слово даже если оно будет написано без пробела или с
            # точкой/запятой (например, "криптовалюта,").
            # re.IGNORECASE - сделает регулярное выражение нечувствительным к регистру.
            if re.search(rf'\b{word}\b', product_name, re.IGNORECASE):
                # Django формы имеют атрибут self.fields['product_name'].label, который хранит читаемое имя поля (то,
                # что будет видно в форме для пользователя, чтоб вывести в предупреждении потом красиво.)
                field_label = self.fields['product_name'].label
                raise ValidationError(f'Поле "{field_label}" не может содержать это слово')
        return product_name

    def clean_description(self):
        """Валидация атрибута формы 'description', которая проверяет отсутствие запрещенных слов в данном поле."""
        description = self.cleaned_data.get('description', '')
        for word in FORBIDDEN_WORDS:
            if re.search(rf'\b{word}\b', description, re.IGNORECASE):
                field_label = self.fields['description'].label
                raise ValidationError(f'Поле "{field_label}" не может содержать это слово')
        return description

    def clean_price(self):
        """Валидация атрибута формы 'price', которая проверяет что цена не отрицательная."""
        price = self.cleaned_data.get('price')
        if price < 0:
            field_label = self.fields['price'].label
            raise ValidationError(f'Поле "{field_label}" не может быть отрицательным.')
        return price

    def clean_image(self):
        """Валидацию формата (JPEG/PNG) и размера (до 5 МБ) загружаемого пользователем изображения."""
        image = self.cleaned_data.get('image')
        if image:
            if image.content_type not in ALLOWED_IMAGE_FORMATS:
                raise ValidationError('Файл должен быть в формате JPEG или PNG.')
            if image.size > MAX_IMAGE_SIZE:
                raise ValidationError('Размер изображения не должен превышать 5 МБ.')
        return image


class ContactForm(forms.Form):
    """Форма для заполнения и отправки пользователем обратной связи на странице contacts.html."""
    name = forms.CharField(max_length=100, label="Имя", required=True)
    phone = forms.CharField(max_length=15, label="Телефон", required=True)
    message = forms.CharField(widget=forms.Textarea, label="Сообщение", required=True)
