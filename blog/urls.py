from django.urls import path
from . import views

app_name = "Blog"

urlpatterns = [
    path('home/', views.BlogListView.as_view(), name='blog_page'),
    path('article/<int:pk>/', views.BlogDetailView.as_view(), name='article_detail_page'),
    path('add_article/', views.BlogCreateView.as_view(), name='add_your_article_page'),
    path('update/<int:pk>/', views.BlogUpdateView.as_view(), name='add_your_article_page'),
    path('delete/<int:pk>/', views.BlogDeleteView.as_view(), name='article_confirm_delete_page'),
]