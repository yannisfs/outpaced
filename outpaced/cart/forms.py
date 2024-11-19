# cart/forms.py

from django import forms

class CartAddProductForm(forms.Form):
    """
    Form to add a product to the cart with a specified quantity.
    """
    quantity = forms.IntegerField(min_value=1, initial=1)