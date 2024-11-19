# news/views.py

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import NewsItem


class HomePageView(ListView):
    """
    View to display the latest news items on the homepage.
    """
    model = NewsItem
    template_name = 'news/homepage.html'  # Specify your template
    context_object_name = 'news_items'
    paginate_by = 5  # Number of news items per page (optional)

    def get_queryset(self):
        return NewsItem.objects.filter(is_published=True).order_by('-published_date')


class NewsDetailView(DetailView):
    """
    View to display the details of a single news item.
    """
    model = NewsItem
    template_name = 'news/news_detail.html'
    context_object_name = 'news_item'