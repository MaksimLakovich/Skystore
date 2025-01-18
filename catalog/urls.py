from django.urls import path
from catalog.apps import CatalogConfig
from . import views

app_name = CatalogConfig.name

urlpatterns = [
    path('home/', views.home_page, name='home_page'),
    path('contacts/', views.contacts_page, name='contacts_page'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
]