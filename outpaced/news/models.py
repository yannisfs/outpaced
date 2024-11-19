# news/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


class NewsItem(models.Model):
    """
    Model representing a news item on the homepage.
    """
    CATEGORY_CHOICES = [
        ('product', 'New Product'),
        ('update', 'Update'),
        ('event', 'Event'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='news_items')
    content = models.TextField()
    image = models.ImageField(upload_to='news_images/', blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='update')
    published_date = models.DateTimeField(default=timezone.now)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-published_date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news:news_detail', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.slugify_title()
        super().save(*args, **kwargs)

    def slugify_title(self):
        from django.utils.text import slugify
        return slugify(self.title)