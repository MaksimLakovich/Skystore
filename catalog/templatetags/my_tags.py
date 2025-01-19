from django import template

register = template.Library()


@register.filter()
def media_filter(path):
    """Шаблонный фильтр/тег для изображений, который обрабатывает путь из БД и адаптирует его для HTML-страниц.
    :param path: Путь до изображения.
    :return: Адаптированный путь для HTML-страницы."""
    if path:
        path = str(path)
        if path.startswith("media/"):  # Проверяю, начинается ли путь с "media/"
            return f"/{path}"
        else:
            return f"/media/{path}"
    return "#"  # Если путь пустой, возвращаю просто плейсхолдер
