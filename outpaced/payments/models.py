from django.conf import settings
from django.db import models
from orders.models import Order

class Payment(models.Model):
    PAYMENT_METHODS = (
        ('CC', 'Credit Card'),
        ('PP', 'PayPal'),
        # Add more methods as needed
    )
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    method = models.CharField(max_length=2, choices=PAYMENT_METHODS)
    transaction_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    successful = models.BooleanField(default=False)

    def __str__(self):
        return f"Payment {self.transaction_id} for Order {self.order.id}"