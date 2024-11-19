# cart/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from products.models import Product
from .models import Cart, CartItem
from .forms import CartAddProductForm

class CartDetailView(View):
    """
    Display the contents of the cart.
    """
    def get(self, request):
        cart = self.get_cart(request)
        return render(request, 'cart/cart_detail.html', {'cart': cart})

    def get_cart(self, request):
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
            cart, created = Cart.objects.get_or_create(session_key=session_key)
        return cart

class CartAddView(View):
    """
    Add a product to the cart.
    """
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id, available=True)
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            cart = self.get_cart(request)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
            else:
                cart_item.quantity = quantity
                cart_item.save()
            messages.success(request, f"Added {product.name} to your cart.")
        else:
            messages.error(request, "Invalid quantity.")
        return redirect(request.META.get('HTTP_REFERER', 'products:product_list'))

    def get_cart(self, request):
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
            cart, created = Cart.objects.get_or_create(session_key=session_key)
        return cart

class CartRemoveView(View):
    """
    Remove a product from the cart.
    """
    def post(self, request, product_id):
        cart = self.get_cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart_item = CartItem.objects.filter(cart=cart, product=product).first()
        if cart_item:
            cart_item.delete()
            messages.success(request, f"Removed {product.name} from your cart.")
        else:
            messages.error(request, "Product not found in your cart.")
        return redirect('cart:cart_detail')

    def get_cart(self, request):
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
            cart, created = Cart.objects.get_or_create(session_key=session_key)
        return cart

class CartUpdateView(View):
    """
    Update the quantity of a product in the cart.
    """
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        quantity = request.POST.get('quantity')
        if not quantity.isdigit() or int(quantity) < 1:
            messages.error(request, "Invalid quantity.")
            return redirect('cart:cart_detail')

        quantity = int(quantity)
        cart = self.get_cart(request)
        cart_item = CartItem.objects.filter(cart=cart, product=product).first()
        if cart_item:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, f"Updated quantity for {product.name}.")
        else:
            messages.error(request, "Product not found in your cart.")
        return redirect('cart:cart_detail')

    def get_cart(self, request):
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
            cart, created = Cart.objects.get_or_create(session_key=session_key)
        return cart