from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Invoice, InvoiceCounter, Client, Product, InvoiceProduct
from .forms import ProductForm, ClientForm, InvoiceForm, InvoiceProductFormSet
from django.urls import reverse
from datetime import datetime
from django.contrib.auth.decorators import login_required

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
            invoice = form.save()
            print(request.POST)
            productsName = request.POST.getlist("productName[]")
            productsPrice = request.POST.getlist("productPrice[]")
            productsQuantity = request.POST.getlist("productQuantity[]")
            for i in range(len(productsName)):
                InvoiceProduct.objects.create(
                    invoice = invoice,
                    name = productsName[i],
                    price = productsPrice[i],
                    quantity = int(productsQuantity[i])
                )
        return HttpResponseRedirect(reverse("invoices:invoices"))
    else:
        form = InvoiceForm()
    return render(request, "invoices/invoiceForm.html", {"form": form})


# Detail
@login_required()
def invoiceDetail(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    products = invoice.products.all()
    if request.method == "POST":
        form = InvoiceForm(request.POST, instance=invoice)
        formset = InvoiceProductFormSet(request.POST, instance=invoice)
        if form.is_valid() and formset.is_valid():
            invoice = form.save()
            products = formset.save(commit=False)
            for product in products:
                product.invoice = invoice
                product.save()
            return HttpResponseRedirect(reverse("invoices:invoices"))
    else:
        form = InvoiceForm(instance=invoice)
        formset = InvoiceProductFormSet(instance=invoice)

    return render(request, "invoices/invoiceDetail.html", {"form": form, "formset":formset, "invoice":invoice})
    products = invoice.products.all()
    return render(request, "invoices/invoiceDetail.html", {"invoice": invoice, "products": products})

# Delete Invoice
@login_required()
def invoiceDelete(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    if request.method == "POST":
        invoice.delete()
        return HttpResponseRedirect(reverse("invoices:invoices"))
    return render(request, "invoices/invoiceDetail.html", {"invoice": invoice})

# PDF
# def pdf(request, invoice_id):
#     return HttpResponse("Invoice download page.")

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