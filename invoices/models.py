from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime

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
    VALUE_PAYMENT = [
            ("cash", "Gotówka"),
            ("transfer", "Przelew"),
            ("card", "Karta"),
        ]

    invoice_number = models.CharField(max_length=50, unique=True)
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE
    )
    issue_date = models.DateField()
    sale_date = models.DateField()
    payment_method = models.CharField(
        max_length=50,
        choices=VALUE_PAYMENT, 
        default="transfer"
    )
    due_date = models.DateField()
    bank_account = models.CharField(max_length=34, null=True, blank=True)
    total_netto = models.DecimalField(max_digits=10, decimal_places=2)
    total_vat = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_brutto = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def save(self, *args, **kwargs):
        if not self.invoice_number: 
        # compare last invoice number with current date and create new invoice number
            current_year = datetime.now().year
            current_month = f"{datetime.now().month:02}"
            old_invoice_number = InvoiceCounter.objects.filter(client = "Damian").first().highest_number
            invoice_prefix, invoice_year, invoice_month, document_number = old_invoice_number.split("/")
            if(int(invoice_year) == int(current_year) and current_month == invoice_month):
                new_document_number = int(document_number) + 1
                new_invoice_number = f"FV/{current_year}/{current_month}/{new_document_number}"
            else:
                new_invoice_number = f"FV/{current_year}/{current_month}/1"
            
            # save new invoice number in database
            InvoiceCounter.objects.filter(client = "Damian").update(highest_number=new_invoice_number)

            self.invoice_number = new_invoice_number
        super().save(*args, **kwargs)
    def __str__(self):
        return self.invoice_number
    
class InvoiceProduct(models.Model):
    VALUE_TAX = [
        (23, 23),
        (8, 8),
        (7, 7),
        (5, 5),
        (4, 4),
        (0, 0),
    ]
    
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=255) 
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=1)
    tax = models.IntegerField(
        choices=VALUE_TAX,
        default=23
    )
    def __str__(self):
        return f"{self.name} x {self.quantity} ({self.invoice.invoice_number})"
    
# Table: Highest Invoice Number
class InvoiceCounter(models.Model):
    client = models.CharField(max_length=255)
    highest_number = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return f"{self.client}: {self.highest_number}"