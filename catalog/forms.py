from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    """Форма для добавления пользователем нового товара на странице add_your_product.html."""

    class Meta:
        model = Product
        fields = ['product_name', 'description', 'price', 'image', 'category']
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
    # Убираю help_text для всех полей чтоб он на странице не выводился по умолчанию
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.help_text = None


class ContactForm(forms.Form):
    """Форма для заполнения и отправки пользователем обратной связи на странице contacts.html."""
    name = forms.CharField(max_length=100, label="Имя", required=True)
    phone = forms.CharField(max_length=15, label="Телефон", required=True)
    message = forms.CharField(widget=forms.Textarea, label="Сообщение", required=True)
