from django import forms
from .models import Product, Client

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price_netto', 'vat_rate', 'price_brutto']

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'nip_number', 'street', 'city', 'postal_code', 'country', 'phone_number', 'email']
        