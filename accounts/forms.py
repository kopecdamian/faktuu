from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password1", "password2"]

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['nip_number', 'regon_number', 'bank_account_number', 'year', 'street', 'city', 'postal_code', 'country']
        labels = {
            "nip_number":  "NIP",
            "regon_number": "REGON",
            "bank_account_number": "Numer konta",
            "year": "Rok",
            "street": "Ulica",
            "city": "Miasto",
            "postal_code": "Kod pocztowy",
            "country": "Kraj"
        }
        widgets = {
            'nip_number': forms.TextInput(attrs={'class': 'custom-input', 'placeholder': 'Podaj numer bankowy'}),
            'regon_number': forms.TextInput(attrs={'class': 'custom-input', 'placeholder': 'Podaj numer bankowy'}),
            'bank_account_number': forms.TextInput(attrs={'class': 'custom-input', 'placeholder': 'Podaj numer bankowy'}),
            'year': forms.TextInput(attrs={'class': 'custom-input', 'placeholder': 'Podaj numer bankowy'}),
            'street': forms.TextInput(attrs={'class': 'custom-input', 'placeholder': 'Podaj numer bankowy'}),
            'city': forms.TextInput(attrs={'class': 'custom-input', 'placeholder': 'Podaj numer bankowy'}),
            'postal_code': forms.TextInput(attrs={'class': 'custom-input', 'placeholder': 'Podaj numer bankowy'}),
            'country': forms.TextInput(attrs={'class': 'custom-input', 'placeholder': 'Podaj numer bankowy'}),
        }
