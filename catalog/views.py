from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from catalog.models import ContactsData, Product


def home_page(request):
    """Контроллер для отображения домашней страницы (home.html).
    Для отладки контроллер главной/домашней страницы выводит в консоль последние 5 созданных продуктов.
    :param request: Экземпляр класса HttpRequest, который содержит всю информацию о запросе."""
    # Выборка последних 5 продуктов. Символ '-' перед 'created_at' устанавливает порядок от новых к старым.
    # Если не использовать символ '-' перед 'created_at', то порядок будет наоборот от старых к новым.
    latest_products = Product.objects.order_by("-created_at")[:5]
    # Вывод в консоль данных для отладки
    for product in latest_products:
        print(f"Название: {product.product_name}, Дата создания: {product.created_at}")

    return render(request, "catalog/home.html")


def contacts_page(request):
    """Контроллер для отображения страницы с контактной информацией (contacts.html).
    :param request: Экземпляр класса HttpRequest, который содержит всю информацию о запросе."""
    if request.method == "POST":
        name = request.POST.get("name")
        # Если метод запроса POST, контроллер получает данные из формы (name) и возвращает простой HTTP-ответ.
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение успешно отправлено")
    # Если метод запроса — GET, контроллер рендерит шаблон contacts.html
    # Сразу получаю контактные данные из БД, чтоб потом их использовать при рендере шаблона страницы-html
    contacts_data = ContactsData.objects.all()
    return render(request, "catalog/contacts.html", {"contacts_data": contacts_data})


def product_detail(request, pk):
    """Контроллер для отображения страницы с подробной информацией о продукте (product_info.html).
    :param request: Экземпляр класса HttpRequest, который содержит всю информацию о запросе.
    :param pk: ID продукта в БД для получения данных с помощью ORM-запроса."""
    # ВАРИАНТ 1: product_data = Product.objects.get(id=pk)
    # ВАРИАНТ 2: вместо get() можно использовать get_object_or_404(), эта функция или найдет экземпляр по ID в БД,
    # или выведет пользователю ошибку 404, а не системную информацию с ошибкой в коде (это хорошая практика).
    product_data = get_object_or_404(Product, id=pk)
    context = {"product": product_data}
    return render(request, "catalog/product_info.html", context)
