from django import forms

from .models import Article


class ArticleForm(forms.ModelForm):
    """Форма для добавления пользователем новой статьи в блоге на странице add_your_article.html."""

    class Meta:
        model = Article
        fields = ['article_title', 'article_contents', 'image']
        widgets = {
            'article_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите заголовок вашей статьи (max: 100 символов)',
                'required': True,
            }),
            'article_contents': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Напишите текст вашей статьи',
                'required': True,
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
        }
    # Убираю help_text для всех полей чтоб он на странице не выводился по умолчанию
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.help_text = None
