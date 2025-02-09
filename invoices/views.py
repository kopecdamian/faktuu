from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Invoice, InvoiceCounter, Client, Product
from django.urls import reverse
from datetime import datetime

# Create your views here.
# Invoices
def index(request):
    all_invoices = Invoice.objects.all()
    context = {
        "all_invoices": all_invoices,
    }
    return render(request, "invoices/index.html", context)
    
# Create invoice
def forms(request):
    all_clients = Client.objects.all()
    context = {
        "all_clients": all_clients,
    }
    return render(request, "invoices/forms.html", context)

# Save invoice
def save(request):
    if request.method == 'POST':

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
        client = request.POST.get('client')
        product = request.POST.get('product')
        
        Invoice.objects.create(
            invoice_number = new_invoice_number,
            client = Client.objects.get(id=client),
            product = product
        )
    return HttpResponseRedirect(reverse("invoices:index"))

# Detail
def detail(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    return render(request, "invoices/detail.html", {"invoice": invoice})

# PDF
def pdf(request, invoice_id):
    return HttpResponse("Invoice download page.")

# clietns
def clients(request):
    all_clients = Client.objects.all()
    context = {
        "all_clients": all_clients,
    }
    return render(request, "invoices/clients.html", context)

# Create New Client
def clientform(request):
    return render(request, "invoices/clientform.html")

# Save New Client
def saveclient(request):
    if request.method == 'POST':

        clientName = request.POST.get('clientName')
        nipNumber = request.POST.get('nipNumber')
        adress = request.POST.get('adress')
        city = request.POST.get('city')
        postalCode = request.POST.get('postalCode')
        country = request.POST.get('country')
        phoneNumber = request.POST.get('phoneNumber')
        email = request.POST.get('email')
        
        Client.objects.create(
            name = clientName,
            nip_number = nipNumber,
            street = adress,
            city = city,
            postal_code = postalCode,
            country = country,
            phone_number = phoneNumber,
            email = email
        )
    return HttpResponseRedirect(reverse("invoices:clients"))

# Client Detail
def clientDetail(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    return render(request, "invoices/clientDetail.html", {"client": client})

# Products
def products(request):
    all_products = Product.objects.all()
    context = {
        "all_products": all_products,
    }
    return render(request, "invoices/products.html", context)

# Create New Product
def productForm(request):
    return render(request, "invoices/productForm.html")

# Save New Product
def productSave(request):
    if request.method == 'POST':

        productName = request.POST.get('productName')
        vatRate = request.POST.get('vatRate')
        priceNetto = request.POST.get('priceNetto')
        priceBrutto = request.POST.get('priceBrutto')
        
        Product.objects.create(
            name = productName,
            vat_rate = vatRate,
            price_netto = priceNetto,
            price_brutto = priceBrutto
        )
    return HttpResponseRedirect(reverse("invoices:products"))

# Product Detail
def productDetail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, "invoices/productDetail.html", {"product": product})