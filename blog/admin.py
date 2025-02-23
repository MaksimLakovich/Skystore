from django.contrib import admin

from blog.models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """Настройка отображения данных модели Article в админке."""
    list_display = ("id", "article_title", "is_published", "create_at")
    list_filter = ("article_title",)
    search_fields = ("article_title", "create_at",)
