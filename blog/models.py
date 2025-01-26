from django.db import models


class Article(models.Model):
    """Модель Article представляет статью для блога в интернет-магазине."""
    article_title = models.CharField(max_length=100, unique=True, blank=False, verbose_name='Заголовок статьи', help_text="Введите заголовок статьи")
    article_contents = models.TextField(blank=False, verbose_name='Содержимое статьи', help_text="Введите содержимое статьи")
    image = models.ImageField(upload_to='article_image/', blank=True, verbose_name='Превью (изображение)', help_text="Добавьте превью")
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_published = models.BooleanField(default=False, blank=False, verbose_name='Признак публикации', help_text="Зафиксируйте факт публикации")
    views_counter = models.PositiveIntegerField(default=0, verbose_name='Количество просмотров')

    def __str__(self):
        """Метод определяет строковое представление объекта. Полезно для отображения объектов в админке/консоли."""
        return f"{self.article_title}"

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ["article_title"]
        db_table = "blog_articles"
