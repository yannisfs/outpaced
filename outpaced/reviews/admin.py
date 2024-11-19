from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'comment')
    list_filter = ('product', 'rating')
    search_fields = ('products', 'rating')