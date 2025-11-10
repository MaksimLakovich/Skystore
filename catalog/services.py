from django.core.cache import cache

from catalog.models import Product


class ProductService:
    """Класс для сервисных функций по работе с продуктами (модель Product)."""

    @staticmethod
    def get_products_by_category(category_id):
        """Функция со встроенным кешированием для получения списка всех продуктов в указанной категории.
        :param category_id: ID категории.
        :return: Список продуктов."""
        cache_key = f"category_products_{category_id}"
        products = cache.get(cache_key)

        if products is None:  # Проверяю есть ли данные в кеше
            products = list(  # Кеширую список (list), а не сам QuerySet так как это более безопасно и стабильно
                Product.objects.filter(category_id=category_id, is_published=True)
                .select_related("category")
                .order_by("-created_at")
            )
            cache.set(cache_key, products, timeout=60 * 15)

        return products
