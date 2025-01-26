from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages

from blog.forms import ArticleForm
from blog.models import Article


class BlogListView(ListView):
    """Представление для отображения домашней страницы (blogs.html) с пагинацией и счетчиком просмотров."""
    model = Article
    template_name = "blog/blogs.html"
    context_object_name = "articles"
    paginate_by = 4


class BlogDetailView(DetailView):
    """Представление для отображения страницы с подробной информацией о статье (article.html)."""
    model = Article
    template_name = "blog/article.html"
    context_object_name = "article"

    def get_object(self, queryset=None):
        """Переопределяю метод get_object() для увеличения счетчика просмотров (views_counter) при каждом просмотре."""
        self.object = super().get_object(queryset)
        self.object.views_counter += 1
        self.object.save()
        return self.object


class BlogCreateView(CreateView):
    """Представление для отображения страницы с формой, которая позволяет пользователю добавить новую статью в блог."""
    model = Article
    template_name = "blog/add_your_article.html"
    # Подключаю свою форму (blog/forms.py/ArticleForm) с тем, что ранее настраивал уже (стили)
    form_class = ArticleForm
    success_url = reverse_lazy("blog:blog_page")

    def form_valid(self, form):
        """Отправка пользователю уведомления о том, что его статья успешно отправлена."""
        # С помощью стандартного механизма Django для уведомлений, отправляю пользователю сообщение
        messages.success(self.request, f"Спасибо! Ваша статья добавлена и появится после проверки модератора.")
        # Возвращаем стандартное поведение формы
        return super().form_valid(form)


class BlogUpdateView(UpdateView):
    """Представление для редактирования статьи в блоге."""
    model = Article
    template_name = "blog/add_your_article.html"
    form_class = ArticleForm
    success_url = reverse_lazy("blog:blog_page")


class BlogDeleteView(DeleteView):
    """Представление для удаления статьи в блоге."""
    model = Article
    template_name = "blog/article_confirm_delete.html"
    success_url = reverse_lazy("blog:blog_page")
    context_object_name = "article"

    def form_valid(self, form):
        """Отправка пользователю уведомления о том, что статья была удалена."""
        # Получаю объект статьи
        article = self.get_object()
        # С помощью стандартного механизма Django для уведомлений, отправляю пользователю сообщение
        messages.success(self.request, f"Вы удалили статью: {article.article_title}")
        # Возвращаем стандартное поведение формы
        return super().form_valid(form)
