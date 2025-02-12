from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Table: Clients
class Client(models.Model):
    name = models.CharField(max_length=255)
    nip_number = models.IntegerField(validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)])
    street = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

# Table: Products
class Product(models.Model):
    name = models.CharField(max_length=255)
    price_netto = models.DecimalField(max_digits=10, decimal_places=2)
    vat_rate = models.IntegerField(
        default=23,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ])
    price_brutto = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

# Table: Invoices
class Invoice(models.Model):
    invoice_number = models.CharField(max_length=50, unique=True)
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE
    )
    total_netto = models.DecimalField(max_digits=10, decimal_places=2)
    total_brutto = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.invoice_number
    
class InvoiceProduct(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="products")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    def __str__(self):
        return f"{self.product.name} x {self.quantity} ({self.invoice.invoice_number})"
    
# Table: Highest Invoice Number
class InvoiceCounter(models.Model):
    client = models.CharField(max_length=255)
    highest_number = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return f"{self.client}: {self.highest_number}"