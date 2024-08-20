from django import forms
from .models import Review, Ticket

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 0, 'max': 10}),
            'comment': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating < 0 or rating > 10:
            raise forms.ValidationError("Rating must be between 0 and 10.")
        return rating

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['ticket_type']

