# reviews/models.py

from django.conf import settings
from django.db import models
from products.models import Product

class Review(models.Model):
    """
    Represents a product review.
    """
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('product', 'user')  # Prevent multiple reviews per user per product

    def __str__(self):
        return f"Review by {self.user.username} on {self.product.name}"