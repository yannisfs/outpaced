# payments/views.py

import stripe
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from orders.models import Order
from django.urls import reverse
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

stripe.api_key = settings.STRIPE_SECRET_KEY

class ProcessPaymentView(View):
    """
    Initiate a Stripe Checkout Session for the given order.
    """
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user, status='P')
        line_items = []
        for item in order.items.all():
            line_items.append({
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': item.product.name,
                        'images': [request.build_absolute_uri(item.product.images.first.image.url) if item.product.images.first else ''],
                    },
                    'unit_amount': int(item.price * 100),  # Stripe expects amount in cents
                },
                'quantity': item.quantity,
            })
        
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url=request.build_absolute_uri(reverse('orders:order_success')),
                cancel_url=request.build_absolute_uri(reverse('orders:order_cancel')),
                metadata={
                    'order_id': order.id
                }
            )
            return redirect(checkout_session.url)
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('orders:checkout')

@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhookView(View):
    """
    Handle Stripe webhook events.
    """
    def post(self, request):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
        event = None

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except ValueError:
            # Invalid payload
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError:
            # Invalid signature
            return HttpResponse(status=400)

        # Handle the checkout.session.completed event
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            order_id = session.get('metadata', {}).get('order_id')
            if order_id:
                try:
                    order = Order.objects.get(id=order_id, status='P')
                    order.status = 'C'
                    order.save()
                except Order.DoesNotExist:
                    pass  # Order already processed or does not exist

        return HttpResponse(status=200)

class PaymentSuccessView(View):
    """
    Display a payment success message.
    """
    def get(self, request):
        return render(request, 'payments/payment_success.html')

class PaymentCancelView(View):
    """
    Display a payment cancellation message.
    """
    def get(self, request):
        return render(request, 'payments/payment_cancel.html')