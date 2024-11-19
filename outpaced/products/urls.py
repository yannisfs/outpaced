# products/urls.py

from django.urls import path
from . import views

app_name = 'products'  # Namespace for the app

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    path('category/<slug:category_slug>/', views.ProductListView.as_view(), name='product_list_by_category'),
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    # Optional: Category list
    # path('categories/', views.CategoryListView.as_view(), name='category_list'),
]