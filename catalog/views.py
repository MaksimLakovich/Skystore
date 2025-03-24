from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.cache import cache
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView, DeleteView, DetailView, FormView, ListView, UpdateView

from catalog.forms import ContactForm, ProductForm
from catalog.models import Category, ContactsData, Feedback, Product
from catalog.services import ProductService


class CatalogListView(ListView):
    """Представление для отображения домашней страницы (home.html) с опубликованными продуктами и пагинацией.
    Для отладки главной/домашней страницы представление выводит в консоль последние 5 созданных продуктов."""

    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products"
    paginate_by = 6

    def get_queryset(self):
        """1) Выбираем только опубликованные продукты и сортируем их от новых к старым.
        2) Для отладки выводим в консоль последние 5 добавленных товаров. Символ '-' перед 'created_at' устанавливает
        порядок от новых к старым. Если не использовать символ '-' перед 'created_at', то порядок будет наоборот."""
        queryset = Product.objects.filter(is_published=True).order_by("-created_at")
        latest_products = queryset[:5]
        for product in latest_products:
            print(f"Название: {product.product_name}, Дата создания: {product.created_at}")
        return queryset  # Возвращает только опубликованные продукты


@method_decorator(cache_page(60 * 15), name="dispatch")  # Декоратор для создания кеша для всей страницы
class CatalogDetailView(LoginRequiredMixin, DetailView):
    """Представление для отображения страницы с подробной информацией о продукте (product.html)."""

    model = Product
    template_name = "catalog/product.html"
    context_object_name = "product"


class CatalogCreateView(LoginRequiredMixin, CreateView):
    """Представление для отображения страницы с формой, которая позволяет пользователю добавлять новые товары в БД."""

    model = Product
    form_class = ProductForm
    template_name = "catalog/add_your_product.html"
    success_url = reverse_lazy("catalog:home_page")

    def form_valid(self, form):
        """1) Отправка пользователю уведомления о том, что его продукт успешно добавлен.
        2) Автоматическое заполнение текущим пользователем поля 'owner' при создании нового продукта."""
        form.instance.owner = self.request.user  # Привязываю текущего пользователя как owner
        # С помощью стандартного механизма Django для уведомлений, отправляю пользователю сообщение
        messages.success(self.request, f"Спасибо! Ваш продукт успешно добавлен.")
        # Возвращаю стандартное поведение формы
        return super().form_valid(form)

    def get_form_kwargs(self):
        """Передаю текущего пользователя в форму."""
        kwargs = super().get_form_kwargs()
        kwargs["initial"] = {"owner": self.request.user} # Передаём текущего пользователя, чтоб он сразу отображался
        return kwargs


class CatalogUpdateView(LoginRequiredMixin, UpdateView):
    """Представление для редактирования продукта в магазине."""

    model = Product
    form_class = ProductForm
    template_name = "catalog/add_your_product.html"

    def dispatch(self, request, *args, **kwargs):
        """Метод выполняет проверку прав пользователя на редактирование продукта (владелец продукта), заранее до
        выполнения любого запроса (GET, POST и т.д.)."""
        product = get_object_or_404(Product, pk=self.kwargs["pk"])
        if not request.user == product.owner:
            return HttpResponseForbidden(
                f"У вас нет прав для редактирования продукта. Обратитесь к владельцу: {product.owner}"
            )
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        """Перенаправление на страницу с деталями продукта после успешного редактирования."""
        return reverse("catalog:product_detail_page", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        """Метод сброса кеша страницы CatalogDetailView по URL при изменении каких-либо параметров продукта."""
        response = super().form_valid(form)
        # Формирую URL, который кеширует CatalogDetailView
        product_url = reverse("catalog:product_detail_page", kwargs={"pk": self.object.pk})
        cache.delete(product_url)  # Удаляю кеш по URL после обновления продукта
        return response


class CatalogDeleteView(LoginRequiredMixin, DeleteView):
    """Представление для удаления продукта в магазине."""

    model = Product
    template_name = "catalog/product_confirm_delete.html"
    context_object_name = "product"
    success_url = reverse_lazy("catalog:home_page")

    object: Product  # Добавляю явную аннотацию чтоб не ругался MYPY

    def dispatch(self, request, *args, **kwargs):
        """Метод выполняет проверку прав пользователя на удаление продукта (владелец или модератор),
        заранее до выполнения любого запроса (GET, POST и т.д.)."""
        product = get_object_or_404(Product, pk=self.kwargs["pk"])
        if request.user.has_perm("catalog.delete_product") or request.user == product.owner:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden(
            f"У вас нет прав для удаления продукта. Обратитесь к владельцу ({product.owner}) или модераторам магазина."
        )

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
        Feedback.objects.create(name=name, phone=phone, message=message)
        # С помощью стандартного механизма Django для уведомлений, отправляю пользователю сообщение
        messages.success(self.request, f"Спасибо, {name}! Ваше сообщение успешно отправлено.")
        # Возвращаем стандартное поведение формы
        return super().form_valid(form)


class CatalogPublicationView(PermissionRequiredMixin, View):
    """Представление Модератора для управления публикациями продуктов в магазине ('Опубликовать' / 'Отменить')."""

    # Устанавливаю для PermissionRequired, что требуется именно право 'can_change_product_publication':
    permission_required = "catalog.can_change_product_publication"

    def post(self, request, pk):
        """Метод обрабатывает POST-запрос на то, чтоб опубликовать или отменить публикацию продукта."""
        product = get_object_or_404(Product, pk=pk)
        if not request.user.has_perm("catalog.can_change_product_publication"):
            return HttpResponseForbidden("У вас нет прав на управление публикациями продуктов.")
        # Эта строка автоматически меняет статус публикации: если был True → станет False и наоборот. Удобно тем, что
        # теперь и публиковать и отменять публикацию можно одним контроллером CatalogPublicationView, а не отдельными.
        product.is_published = not product.is_published
        product.save()
        return redirect("catalog:unpublished_products_page")


class CatalogUnpublishedListView(PermissionRequiredMixin, ListView):
    """Представление для страницы с неопубликованными продуктами (unpublished_products.html) с пагинацией."""

    model = Product
    template_name = "catalog/unpublished_products.html"
    context_object_name = "products"
    paginate_by = 6

    permission_required = "catalog.can_change_product_publication"  # Ограничиваю доступ, чтоб только Модератор мог

    def get_queryset(self):
        """Выбираем только неопубликованные продукты и сортируем их от новых к старым"""
        return Product.objects.filter(is_published=False).order_by("-created_at")


class CatalogCategoryProductsView(ListView):
    """Представление для отображения списка всех опубликованных продуктов в указанной категории (с пагинацией)."""

    model = Product
    template_name = "catalog/category_products.html"
    context_object_name = "products"
    paginate_by = 6

    def get_queryset(self):
        """Выбираем с помощью сервисной функции все продукты в указанной категории, если категория выбрана."""
        category_id = self.kwargs.get("category_id")  # Получаю ID категории из URL
        if category_id:
            return ProductService.get_products_by_category(category_id)
        return Product.objects.none()  # Если категория не выбрана, возвращаю пустой QuerySet

    def get_context_data(self, **kwargs):
        """Добавляем список категорий и текущую категорию в контекст шаблона."""
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()  # Передаем список всех категорий
        category_id = self.kwargs.get("category_id")
        if category_id:
            context["selected_category"] = Category.objects.get(pk=category_id)
        return context
