# reviews/forms.py

from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    """
    Form to submit a product review.
    """
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-select'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }