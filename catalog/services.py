from catalog.models import Product


class ProductService:
    """Класс для сервисных функций по работе с продуктами (модель Product)."""

    @staticmethod
    def get_products_by_category(category_id):
        """Функция для получения списка всех продуктов в указанной категории.
        :param category_id: ID категории.
        :return: Список продуктов."""
        products = (
            Product.objects.filter(category_id=category_id, is_published=True)
            .select_related("category")
            .order_by("-created_at")
        )
        return products
