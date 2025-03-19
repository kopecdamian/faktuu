from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['nip_number', 'regon_number', 'bank_account_number']