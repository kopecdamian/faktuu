from django import forms
from django.forms import inlineformset_factory
from .models import Product, Client, Invoice, InvoiceProduct

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price_netto', 'vat_rate', 'price_brutto']

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'nip_number', 'street', 'city', 'postal_code', 'country', 'phone_number', 'email']

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['client']

class InvoiceProductForm(forms.ModelForm):
    class Meta:
        model = InvoiceProduct
        fields = ['name', 'price', 'quantity']

InvoiceProductFormSet = inlineformset_factory(
    Invoice, 
    InvoiceProduct,
    form=InvoiceProductForm,
    extra=1, 
    can_delete=False 
)