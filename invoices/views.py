from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from .models import Invoice, InvoiceCounter, Client, Product, InvoiceProduct
from .forms import ProductForm, ClientForm, InvoiceForm, InvoiceProductFormSet
from django.urls import reverse
from datetime import datetime
from django.contrib.auth.decorators import login_required
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

# Create your views here.
# Invoices
@login_required()
def invoices(request):
    all_invoices = Invoice.objects.all()
    context = {
        "all_invoices": all_invoices,
    }
    return render(request, "invoices/invoices.html", context)
    
# Create invoice
@login_required()
def invoiceForm(request):
    if request.method == "POST":
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save(commit=False)
            invoice.total_netto = request.POST.get('totalNetto')
            invoice = form.save()
            productsName = request.POST.getlist("productName[]")
            productsPrice = request.POST.getlist("productPrice[]")
            productsTax = request.POST.getlist("productTax[]")
            productsQuantity = request.POST.getlist("productQuantity[]")
            for index in range(len(productsName)):
                InvoiceProduct.objects.create(
                    invoice = invoice,
                    name = productsName[index],
                    price = productsPrice[index],
                    tax = productsTax[index],
                    quantity = int(productsQuantity[index])
                )
        return HttpResponseRedirect(reverse("invoices:invoices"))
    else:
        form = InvoiceForm()
    return render(request, "invoices/invoiceForm.html", {"form": form})


# Detail
@login_required()
def invoiceDetail(request, invoice_id):
    # get invoice data
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    products = invoice.products.all()
    # update invoice data
    if request.method == "POST":
        form = InvoiceForm(request.POST, instance=invoice)
        print(request.POST)
        if form.is_valid():
            print('valid')
            invoice = form.save(commit=False)
            invoice.total_netto = request.POST.get('totalNetto')
            invoice = form.save()
            id_existing_products = []
            id_updated_product = []
            # add invoiceProduct id to list
            for product in products:
                id_existing_products.append(product.id)
            # get data from form
            productsId = request.POST.getlist("productId[]")
            productsName = request.POST.getlist("productName[]")
            productsPrice = request.POST.getlist("productPrice[]")
            productsTax = request.POST.getlist("productTax[]")
            productsQuantity = request.POST.getlist("productQuantity[]")
            for index in range(len(productsName)):
                # update existing invoiceProduct
                print(productsId)
                if productsId[index] in id_existing_products:
                    product = products.filter(id=productsId).first()
                    product.name = productsId[index]
                    product.price = productsPrice[index]
                    product.quantity = productsQuantity[index]
                    product.save()
                    id_updated_product.append(productsId[index])
                # create new invoiceProduct
                else:
                    InvoiceProduct.objects.create(
                        invoice = invoice,
                        name = productsName[index],
                        price = productsPrice[index],
                        tax = productsTax[index],
                        quantity = int(productsQuantity[index])
                    )
            # delete invoiceProduct which was deleted in form
            for id_exist in id_existing_products:
                if id_exist not in id_updated_product:
                    products.filter(id=id_exist).first().delete()
            return HttpResponseRedirect(reverse("invoices:invoices"))
    # show invoice data
    else:
        form = InvoiceForm(instance=invoice)
    return render(request, "invoices/invoiceForm.html", {"form": form, "products":products, "invoice":invoice})

# Delete Invoice
@login_required()
def invoiceDelete(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    if request.method == "POST":
        invoice.delete()
        return HttpResponseRedirect(reverse("invoices:invoices"))
    return render(request, "invoices/invoiceDetail.html", {"invoice": invoice})

# PDF
@login_required()
def pdf(request, invoice_id):
    # Pobierz fakturę z bazy danych (przykładowe pobranie)
    invoice = Invoice.objects.get(id=invoice_id)
    products = invoice.products.all()
    
    # Bufor w pamięci do przechowywania PDF
    buffer = io.BytesIO()
    
    # Tworzenie obiektu PDF
    p = canvas.Canvas(buffer, pagesize=A4)
    
    # Dodanie nagłówka faktury
    p.drawString(100, 800, f"Faktura nr: {invoice.invoice_number}")
    p.drawString(100, 780, f"Data wystawienia: {invoice.issue_date}")
    p.drawString(100, 760, f"Klient: {invoice.client.name}")
    
    # Dodanie produktów z faktury
    y_position = 730
    for product in products:
        p.drawString(100, y_position, f"{product.name} - {product.quantity} x {product.price} PLN")
        y_position -= 20  # Przesunięcie w dół dla kolejnych produktów
    
    # Zamknięcie dokumentu PDF
    p.showPage()
    p.save()
    
    # Przesunięcie wskaźnika na początek bufora
    buffer.seek(0)
    
    # Zwrot pliku jako odpowiedzi HTTP do pobrania
    return FileResponse(buffer, as_attachment=True, filename=f"faktura_{invoice.invoice_number}.pdf")

# clients
@login_required()
def clients(request):
    all_clients = Client.objects.all()
    context = {
        "all_clients": all_clients,
    }
    return render(request, "invoices/clients.html", context)

# Create New Client
@login_required()
def clientform(request):
    if request.method == "POST":
        form = ClientForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("invoices:clients"))
    else:
        form = ClientForm()

    return render(request, "invoices/clientform.html", {"form": form})

# Client Detail
@login_required()
def clientDetail(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == "POST":
        form = ClientForm(request.POST, instance=client)  
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("invoices:clients"))
    else:
        form = ClientForm(instance=client)
    return render(request, "invoices/clientDetail.html", {"form":form, "client": client})

# Delete Client
@login_required()
def clientDelete(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == "POST":
        client.delete()
        return HttpResponseRedirect(reverse("invoices:clients"))
    return render(request, "invoices/clientDetail.html", {"client": client})

# Products
@login_required()
def products(request):
    all_products = Product.objects.all()
    context = {
        "all_products": all_products,
    }
    return render(request, "invoices/products.html", context)

# Create New Product
@login_required()
def productForm(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("invoices:products"))
    else:
        form = ProductForm()

    return render(request, "invoices/productForm.html", {"form": form})

# Product Detail
@login_required()
def productDetail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)  
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("invoices:products"))
    else:
        form = ProductForm(instance=product)
    return render(request, "invoices/productDetail.html", {"form": form, "product":product})

# Delete Product
@login_required()
def productDelete(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == "POST":
        product.delete()
        return HttpResponseRedirect(reverse("invoices:products"))
    return render(request, "invoices/productDetail.html", {"product": product})