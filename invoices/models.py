from django.db import models

# Create your models here.
# Table: Clients
class Client(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

# Table: Products
class Product(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

# Table: Invoices
# class Invoice(models.Model):
#     invoice_number = models.CharField(max_length=50, unique=True)
#     client = models.ForeignKey(Client, on_delete=models.CASCADE)