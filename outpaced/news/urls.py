# news/urls.py

from django.urls import path
from .views import HomePageView, NewsDetailView

app_name = 'news'

urlpatterns = [
    path('', HomePageView.as_view(), name='homepage'),  # Homepage view
    path('<slug:slug>/', NewsDetailView.as_view(), name='news_detail'),  # Detail view
]