from django.db import models

# Create your models here.
# Table: Clients
class Client(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

# Table: Products
class Product(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

# Table: Invoices
class Invoice(models.Model):
    invoice_number = models.CharField(max_length=50, unique=True)
    client = models.CharField(max_length=255)
    product = models.CharField(max_length=255)
    def __str__(self):
        return self.invoice_number