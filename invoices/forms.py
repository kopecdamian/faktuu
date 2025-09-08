from django import forms
from django.forms import inlineformset_factory
from .models import Product, Client, Invoice, InvoiceProduct

class ProductForm(forms.ModelForm):
    class Meta:
        VALUE_TAX = [
            (23, 23),
            (8, 8),
            (7, 7),
            (5, 5),
            (4, 4),
            (0, 0),
        ]
        model = Product
        fields = ['name', 'tax', 'measurement', 'type', 'price_netto', 'price_brutto', 'currency', 'desc']
        labels = {
            "name":  "Nazwa *",
            "tax": "Podatek VAT *",
            'measurement': 'Jednostka miary *',
            'type': 'Rodzaj *',
            "price_netto": "Cena Netto *",
            "price_brutto": "Cena Brutto *",
            'currency': 'Waluta *',
            'code': 'Kod *',
            'desc': 'Opis'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'custom-input', 'placeholder': 'Podaj nazwę produktu'}),
            'tax': forms.Select(attrs={'class': 'custom-select'}),
            'measurement': forms.TextInput(attrs={'class': 'custom-input', 'placeholder': 'Podaj rodzaj'}),
            'type': forms.Select(attrs={'class': 'custom-select'}),
            'price_netto': forms.TextInput(attrs={'class': 'custom-input', 'placeholder': 'Cena netto'}),
            'price_brutto': forms.TextInput(attrs={'class': 'custom-input', 'placeholder': 'Cena brutto'}),
            'currency': forms.Select(attrs={'class': 'custom-select'}),
            'code': forms.TextInput(attrs={'class': 'custom-input', 'placeholder': 'Kod zostanie wygenerowany automatycznie po zapisaniu.'}),
            'desc': forms.TextInput(attrs={'class': 'custom-input'}),
        }

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'nip_number', 'street', 'city', 'postal_code', 'country', 'phone_number', 'email']
        labels = {
            "name":  "Nazwa *",
            "nip_number": "Numer NIP *",
            "street": "Ulica",
            "city": "Miasto",
            "postal_code": "Kod Pocztowy",
            "country": "Kraj",
            "phone_number": "Numer Telefonu",
            "email": "Adres Email",
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'custom-input', 'placeholder': 'Podaj nazwę klienta'}),
            'nip_number': forms.TextInput(attrs={'class': 'custom-input', 'placeholder': 'Podaj NIP'}),
            'street': forms.TextInput(attrs={'class': 'custom-input', 'placeholder': 'Podaj ulicę'}),
            'city': forms.TextInput(attrs={'class': 'custom-input', 'placeholder': 'Podaj miasto'}),
            'postal_code': forms.TextInput(attrs={'class': 'custom-input', 'placeholder': 'Podaj kod pocztowy'}),
            'country': forms.TextInput(attrs={'class': 'custom-input', 'placeholder': 'Podaj kraj'}),
            'phone_number': forms.TextInput(attrs={'class': 'custom-input', 'placeholder': 'Podaj numer telefonu'}),
            'email': forms.EmailInput(attrs={'class': 'custom-input', 'placeholder': 'Podaj adres e-mail'}),
        }

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['client', 'issue_date', 'sale_date', 'payment_method', 'due_date', 'bank_account']
        labels = {
            "client":  "Nazwa klienta",
            "issue_date": "Data wydania",
            "sale_date": "Data sprzedazy",
            "payment_method": "Sposób płatnośści",
            "due_date": "Termin płatności",
            "bank_account": "Numer bankowy"
        }
        widgets = {
            'client': forms.Select(),
            'issue_date': forms.DateInput(attrs={'type': 'date'}),
            'sale_date': forms.DateInput(attrs={'type': 'date'}),
            'payment_method': forms.Select(),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'bank_account': forms.TextInput(attrs={'class': 'custom-input', 'placeholder': 'Podaj numer bankowy'}),
        }

    # show only clients assigned to the user
    def __init__(self, *args, assignedTo=None, **kwargs):
        super().__init__(*args, **kwargs)
        if assignedTo:
            self.fields["client"].queryset = Client.objects.filter(assigned_to=assignedTo)

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