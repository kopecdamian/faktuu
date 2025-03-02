from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from .models import Invoice, InvoiceCounter, Client, Product, InvoiceProduct
from .forms import ProductForm, ClientForm, InvoiceForm, InvoiceProductFormSet
from django.urls import reverse
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
import io
from xhtml2pdf import pisa

# Invoices
@login_required()
def invoices(request):
    all_invoices = Invoice.objects.all()
    print(request.user)
    context = {
        "all_invoices": all_invoices,
    }
    return render(request, "invoices/invoices.html", context)
    
# Create invoice
@login_required()
def invoiceCreate(request):
    if request.method == "POST":
        form = InvoiceForm(request.POST, assignedTo=request.user)
        if form.is_valid():
            invoice = form.save(commit=False)
            invoice.total_netto = request.POST.get('totalNetto')
            invoice.total_vat = request.POST.get('totalVat')
            invoice.total_brutto = request.POST.get('totalBrutto')
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
        form = InvoiceForm(assignedTo=request.user)
    return render(request, "invoices/invoiceForm.html", {"form": form})


# Detail
@login_required()
def invoiceDetail(request, invoice_id):
    # get invoice data
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    products = invoice.products.all()
    # update invoice data
    if request.method == "POST":
        form = InvoiceForm(request.POST, instance=invoice, assignedTo=request.user)
        print(request.POST)
        if form.is_valid():
            invoice = form.save(commit=False)
            invoice.total_netto = request.POST.get('totalNetto')
            invoice.total_vat = request.POST.get('totalVat')
            invoice.total_brutto = request.POST.get('totalBrutto')
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
        form = InvoiceForm(instance=invoice, assignedTo=request.user)
    return render(request, "invoices/invoiceForm.html", {"form": form, "products":products, "invoice":invoice})

# Delete Invoice
@login_required()
def invoiceDelete(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    if request.method == "POST":
        invoice.delete()
        return HttpResponseRedirect(reverse("invoices:invoices"))
    return render(request, "invoices/invoiceDetail.html", {"invoice": invoice})

# Generate PDF
@login_required()
def generateInvoicePdf(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    products = invoice.products.all()

    # get html template
    template_path = "pdf/invoicePdf.html"
    context = {"invoice": invoice, "products": products}
    template = get_template(template_path)
    html = template.render(context)

    # issue with polish signs, the helpful font is Open Sans
    # convert html to pdf
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="faktura_{invoice.invoice_number}.pdf"'
    pisa_status = pisa.CreatePDF(io.BytesIO(html.encode("UTF-8")), dest=response)

    if pisa_status.err:
        return HttpResponse("Błąd przy generowaniu PDF", status=500)

    return response

# clients
@login_required()
def clients(request):
    all_clients = Client.objects.filter(assigned_to=request.user)
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
            client = form.save(commit=False)
            client.assigned_to = request.user
            client = form.save()
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