from django import forms
from .models import Review, Ticket

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 10}),
            'comment': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating < 1 or rating > 10:
            raise forms.ValidationError("Rating must be between 1 and 10.")
        return rating

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['ticket_type', 'quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={'min': 1}),
        }

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity < 1:
            raise forms.ValidationError("Quantity must be at least 1.")
        return quantity