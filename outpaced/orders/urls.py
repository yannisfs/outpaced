# orders/urls.py

from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('success/', views.OrderSuccessView.as_view(), name='order_success'),
    path('cancel/', views.OrderCancelView.as_view(), name='order_cancel'),
    path('history/', views.OrderHistoryView.as_view(), name='order_history'),
    path('detail/<int:order_id>/', views.OrderDetailView.as_view(), name='order_detail'),
]