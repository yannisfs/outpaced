# orders/forms.py

from django import forms

class CheckoutForm(forms.Form):
    """
    Form to collect shipping and payment information during checkout.
    """
    address = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    city = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    postal_code = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    country = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    payment_method = forms.ChoiceField(choices=[
        ('CC', 'Credit Card'),
        ('PP', 'PayPal'),
        # Add more methods as needed
    ], widget=forms.Select(attrs={'class': 'form-select'}))