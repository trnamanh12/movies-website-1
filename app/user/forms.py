# app/user/forms.py
from django import forms
from django.contrib.auth.models import User

class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'date_joined']
        widgets = {
            'date_joined': forms.DateInput(attrs={'readonly': 'readonly'}),
            'username': forms.TextInput(attrs={'readonly': 'readonly'}),
        }