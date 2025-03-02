from catalog.models import Product

def unpublished_products_count(request):
    """Контекстный процессор для автоматического подсчета количества неопубликованных продуктов и передачи
    этого количества во все шаблоны (страницы) магазина."""
    return {"unpublished_count": Product.objects.filter(is_published=False).count()}
