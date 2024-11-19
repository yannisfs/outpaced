# orders/views.py

from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from cart.models import Cart, CartItem
from .models import Order, OrderItem
from .forms import CheckoutForm
from django.urls import reverse
from decimal import Decimal

class CheckoutView(LoginRequiredMixin, View):
    """
    Handle the checkout process.
    """
    def get(self, request):
        cart = self.get_cart(request)
        if not cart.items.exists():
            messages.error(request, "Your cart is empty.")
            return redirect('products:product_list')
        form = CheckoutForm()
        return render(request, 'orders/checkout.html', {'form': form, 'cart': cart})

    def post(self, request):
        cart = self.get_cart(request)
        if not cart.items.exists():
            messages.error(request, "Your cart is empty.")
            return redirect('products:product_list')
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Extract form data
            address = form.cleaned_data['address']
            city = form.cleaned_data['city']
            postal_code = form.cleaned_data['postal_code']
            country = form.cleaned_data['country']
            payment_method = form.cleaned_data['payment_method']
            
            # Calculate total
            total = cart.get_total_price()
            
            # Create Order
            order = Order.objects.create(
                user=request.user,
                status='P',
                total=Decimal(total)
            )
            
            # Create OrderItems
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
            
            # Clear the cart
            cart.items.all().delete()
            
            # Redirect to payment processing
            if payment_method == 'CC':
                # Redirect to payment page (to be implemented)
                return redirect('payments:process_payment', order_id=order.id)
            elif payment_method == 'PP':
                # Redirect to PayPal payment page (to be implemented)
                return redirect('payments:process_payment', order_id=order.id)
            else:
                messages.error(request, "Invalid payment method selected.")
                return redirect('orders:checkout')
        else:
            messages.error(request, "Please correct the errors below.")
            return render(request, 'orders/checkout.html', {'form': form, 'cart': cart})

    def get_cart(self, request):
        cart = Cart.objects.filter(user=request.user).first()
        if not cart:
            cart = Cart.objects.create(user=request.user)
        return cart

class OrderSuccessView(LoginRequiredMixin, View):
    """
    Display order success message.
    """
    def get(self, request):
        return render(request, 'orders/order_success.html')

class OrderCancelView(LoginRequiredMixin, View):
    """
    Display order cancellation message.
    """
    def get(self, request):
        return render(request, 'orders/order_cancel.html')

class OrderHistoryView(LoginRequiredMixin, View):
    """
    Display a list of the user's past orders.
    """
    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by('-created')
        return render(request, 'orders/order_history.html', {'orders': orders})

class OrderDetailView(LoginRequiredMixin, View):
    """
    Display details of a specific order.
    """
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)
        return render(request, 'orders/order_detail.html', {'order': order})