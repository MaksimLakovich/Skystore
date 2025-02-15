 # # ВАРИАНТ 1: импорты для FBV (function-based view):
# from django.core.paginator import Paginator
# from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponse
#
# from catalog.forms import ProductForm
# from catalog.models import ContactsData, Product
#
#
# # ВАРИАНТ 1: использование FBV (function-based view):
# def home_page(request):
#     """Контроллер для отображения домашней страницы (home.html) с пагинацией.
#     Для отладки контроллер главной/домашней страницы выводит в консоль последние 5 созданных продуктов.
#     :param request: Экземпляр класса HttpRequest, который содержит всю информацию о запросе."""
#     # Выборка последних 5 продуктов. Символ '-' перед 'created_at' устанавливает порядок от новых к старым.
#     # Если не использовать символ '-' перед 'created_at', то порядок будет наоборот от старых к новым.
#     latest_products = Product.objects.order_by("-created_at")[:5]
#     # Вывод в консоль данных для отладки:
#     for product in latest_products:
#         print(f"Название: {product.product_name}, Дата создания: {product.created_at}")
#     # Создание контекста:
#     products = Product.objects.all()
#     # Указываю сколько товаров будет отображаться на одной странице:
#     items_per_page = 6
#     # Создаю пагинатор:
#     paginator = Paginator(products, items_per_page)
#     # Получаю номер текущей страницы из GET-запроса (по умолчанию страница 1):
#     page_number = request.GET.get("page", 1)
#     # Получаю продукты для текущей страницы:
#     products = paginator.get_page(page_number)
#     return render(request, "catalog/home.html", {"products": products})
#
#
# def contacts_page(request):
#     """Контроллер для отображения страницы с контактной информацией (contacts.html).
#     :param request: Экземпляр класса HttpRequest, который содержит всю информацию о запросе."""
#     if request.method == "POST":
#         name = request.POST.get("name")
#         # Если метод запроса POST, контроллер получает данные из формы (name) и возвращает простой HTTP-ответ.
#         return HttpResponse(f"Спасибо, {name}! Ваше сообщение успешно отправлено")
#     # Если метод запроса — GET, контроллер рендерит шаблон contacts.html
#     # Сразу получаю контактные данные из БД, чтоб потом их использовать при рендере шаблона страницы-html
#     contacts_data = ContactsData.objects.get(id=1)
#     return render(request, "catalog/contacts.html", {"contacts_data": contacts_data})
#
#
# def product_detail(request, pk):
#     """Контроллер для отображения страницы с подробной информацией о продукте (product.html).
#     :param request: Экземпляр класса HttpRequest, который содержит всю информацию о запросе.
#     :param pk: ID продукта в БД для получения данных с помощью ORM-запроса."""
#     # ВАРИАНТ 1: product_data = Product.objects.get(id=pk)
#     # ВАРИАНТ 2: вместо get() можно использовать get_object_or_404(), эта функция или найдет экземпляр по ID в БД,
#     # или выведет пользователю ошибку 404, а не системную информацию с ошибкой в коде (это хорошая практика).
#     product_data = get_object_or_404(Product, pk=pk)
#     context = {"product": product_data}
#     return render(request, "catalog/product.html", context)
#
#
# def add_product_page(request):
#     """Контроллер для отображения страницы с формой, которая позволяет пользователю добавлять новые товары в БД.
#     :param request: Экземпляр класса HttpRequest, который содержит всю информацию о запросе."""
#     if request.method == "POST":
#         # Вызываю форму для добавления пользователем нового товара (форма создана в forms.py)
#         form = ProductForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponse("Данные Вашего продукта успешно добавлены в магазин. Спасибо!")
#     else:
#         form = ProductForm()
#     return render(request, "catalog/add_your_product.html", {"form": form})


# ВАРИАНТ 2: импорты для CBV (class-based view):
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, FormView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib import messages

from catalog.forms import ContactForm, ProductForm
from catalog.models import ContactsData, Product, Feedback


# ВАРИАНТ 2: использование CBV (class-based view):
class CatalogListView(ListView):
    """Представление для отображения домашней страницы (home.html) с пагинацией.
    Для отладки главной/домашней страницы представление выводит в консоль последние 5 созданных продуктов."""
    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products"
    paginate_by = 6

    def get_queryset(self):
        """Выборка последних 5 продуктов и вывод в консоль. Символ '-' перед 'created_at' устанавливает порядок от
        новых к старым. Если не использовать символ '-' перед 'created_at', то порядок будет наоборот."""
        queryset = Product.objects.order_by("-created_at")
        latest_products = queryset[:5]
        for product in latest_products:
            print(f"Название: {product.product_name}, Дата создания: {product.created_at}")
        return super().get_queryset()


class CatalogDetailView(DetailView):
    """Представление для отображения страницы с подробной информацией о продукте (product.html)."""
    model = Product
    template_name = "catalog/product.html"
    context_object_name = "product"


class CatalogCreateView(CreateView):
    """Представление для отображения страницы с формой, которая позволяет пользователю добавлять новые товары в БД."""
    model = Product
    form_class = ProductForm
    template_name = "catalog/add_your_product.html"
    success_url = reverse_lazy("catalog:home_page")

    def form_valid(self, form):
        """Отправка пользователю уведомления о том, что его продукт успешно добавлен."""
        # С помощью стандартного механизма Django для уведомлений, отправляю пользователю сообщение
        messages.success(self.request, f"Спасибо! Ваш продукт успешно добавлен.")
        # Возвращаем стандартное поведение формы
        return super().form_valid(form)


class CatalogUpdateView(UpdateView):
    """Представление для редактирования продукта в магазине."""
    model = Product
    form_class = ProductForm
    template_name = "catalog/add_your_product.html"

    def get_success_url(self):
        """Перенаправление на страницу с деталями продукта после успешного редактирования."""
        return reverse("catalog:product_detail_page", kwargs={"pk": self.object.pk})


class CatalogDeleteView(DeleteView):
    """Представление для удаления продукта в магазине."""
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    context_object_name = "product"
    success_url = reverse_lazy("catalog:home_page")

    def form_valid(self, form):
        """Отправка пользователю уведомления о том, что продукт был удален."""
        # Получаю объект продукт
        product = self.get_object()
        # С помощью стандартного механизма Django для уведомлений, отправляю пользователю сообщение
        messages.success(self.request, f"Вы удалили продукт: {product.product_name}")
        # Возвращаем стандартное поведение формы
        return super().form_valid(form)


class CatalogContactsView(FormView):
    """Представление для отображения страницы с контактной информацией (contacts.html) и получением от
    пользователя обратной связи."""
    model = ContactsData
    template_name = "catalog/contacts.html"
    # Использую форму из 'catalog/forms.py' для заполнения и отправки пользователем обратной связи на странице
    form_class = ContactForm
    success_url = reverse_lazy("catalog:home_page")

    def get_context_data(self, **kwargs):
        """Добавление данных модели ContactsData (контактные данные из БД) в контекст шаблона."""
        # Добавляю данные из модели ContactsData в контекст:
        context = super().get_context_data(**kwargs)
        # Меняю базовое наименование объекта на 'contacts_data', чтоб не менять код на странице contacts.html, так
        # как эта страница уже использует название 'contacts_data':
        context["contacts_data"] = get_object_or_404(ContactsData, id=1)
        return context

    def form_valid(self, form):
        """Добавление отзыва пользователя в БД (модель Feedback) и отправка пользователю уведомления о том,
        что его обратная связь успешно отправлена."""
        # Логика обработки данных формы
        name = form.cleaned_data["name"]
        phone = form.cleaned_data["phone"]
        message = form.cleaned_data["message"]
        # Сохраняю данные в модель Feedback (таблица 'catalog_feedback' в БД)
        Feedback.objects.create(
            name=name,
            phone=phone,
            message=message
        )
        # С помощью стандартного механизма Django для уведомлений, отправляю пользователю сообщение
        messages.success(self.request, f"Спасибо, {name}! Ваше сообщение успешно отправлено.")
        # Возвращаем стандартное поведение формы
        return super().form_valid(form)
