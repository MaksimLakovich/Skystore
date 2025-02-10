from django.urls import path
from catalog.apps import CatalogConfig
from . import views

app_name = CatalogConfig.name

# # ВАРИАНТ 1: использование FBV (function-based view):
# urlpatterns = [
#     path('home/', views.home_page, name='home_page'),
#     path('contacts/', views.contacts_page, name='contacts_page'),
#     path('product/<int:pk>/', views.product_detail, name='product_detail'),
#     path('add', views.add_product_page, name='add_your_product_page'),
# ]

# ВАРИАНТ 2: использование CBV (class-based view):
urlpatterns = [
    path('home/', views.CatalogListView.as_view(), name='home_page'),
    path('product/<int:pk>/', views.CatalogDetailView.as_view(), name='product_detail'),
    path('add_product/', views.CatalogCreateView.as_view(), name='add_your_product_page'),
    path('contacts/', views.CatalogContactsView.as_view(), name='contacts_page'),
]