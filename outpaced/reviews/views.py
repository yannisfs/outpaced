# reviews/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from products.models import Product
from .forms import ReviewForm
from .models import Review

class AddReviewView(LoginRequiredMixin, View):
    """
    Handle adding a review to a product.
    """
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id, available=True)
        form = ReviewForm(request.POST)
        if form.is_valid():
            # Check if the user has already reviewed the product
            existing_review = Review.objects.filter(product=product, user=request.user).first()
            if existing_review:
                messages.error(request, "You have already reviewed this product.")
                return redirect('products:product_detail', slug=product.slug)
            
            # Create the review
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, "Your review has been submitted.")
            return redirect('products:product_detail', slug=product.slug)
        else:
            messages.error(request, "There was an error with your review submission.")
            return redirect('products:product_detail', slug=product.slug)