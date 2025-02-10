from django.contrib import admin

# Register your models here.
from .models import Client, Product, Invoice, InvoiceCounter, InvoiceProduct

admin.site.register(Client)
admin.site.register(Product)
admin.site.register(Invoice)
admin.site.register(InvoiceProduct)
admin.site.register(InvoiceCounter)