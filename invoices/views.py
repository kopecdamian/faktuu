from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, FileResponse, HttpResponseForbidden, JsonResponse
from .models import Invoice, InvoiceCounter, Client, Product, InvoiceProduct
from .forms import ProductForm, ClientForm, InvoiceForm, InvoiceProductFormSet
from django.urls import reverse
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.db.models import Q
import io
from xhtml2pdf import pisa

# Invoices
@login_required()
def invoices(request):
    all_invoices = Invoice.objects.filter(assigned_to=request.user)
    print(request.user)
    context = {
        "all_invoices": all_invoices,
    }
    return render(request, "invoices/invoices.html", context)
    
# Create invoice
@login_required()
def invoiceCreate(request):
    createdProducts = Product.objects.filter(assigned_to=request.user)
    print(createdProducts)
    if request.method == "POST":
        form = InvoiceForm(request.POST, assignedTo=request.user)
        if form.is_valid():
            invoice = form.save(commit=False)
            invoice.total_netto = request.POST.get('totalNetto')
            invoice.total_vat = request.POST.get('totalVat')
            invoice.total_brutto = request.POST.get('totalBrutto')
            invoice.assigned_to = request.user
            print(request.user)
            invoice.save(user=request.user)
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
    return render(request, "invoices/invoiceForm.html", {"form": form, "createdProducts": createdProducts})


# Detail
@login_required()
def invoiceDetail(request, invoice_id):
    # get invoice data
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    createdProducts = Product.objects.filter(assigned_to=request.user)
    print(createdProducts)
    if invoice.assigned_to != request.user:
        return HttpResponseRedirect(reverse("invoices:invoices"))
    else:
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
        return render(request, "invoices/invoiceForm.html", {"form": form, "products":products, "invoice":invoice, "createdProducts": createdProducts})

# Delete Invoice
@login_required()
def invoiceDelete(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    if invoice.assigned_to != request.user:
        return HttpResponseRedirect(reverse("invoices:invoices"))
    else:
        if request.method == "POST":
            invoice.delete()
            return HttpResponseRedirect(reverse("invoices:invoices"))
        return render(request, "invoices/invoiceDetail.html", {"invoice": invoice})

# Generate PDF
@login_required()
def generateInvoicePdf(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    if invoice.assigned_to != request.user:
        return HttpResponseRedirect(reverse("invoices:invoices"))
    else:
        products = invoice.products.all()

        # get html template
        template_path = "pdf/invoicePdf.html"
        context = {"invoice": invoice, "products": products, "user": request.user}
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
    
# Filter Invoices
@login_required()
def filterInvoices(request):
    query = request.GET.get("query", "").strip()
    if not query: 
        invoices = Invoice.objects.filter(assigned_to=request.user)
    else: 
        invoices = Invoice.objects.filter(
            Q(assigned_to=request.user) & (
                Q(invoice_number__icontains=query) |
                Q(client__name__icontains=query)
            )
        )

    print(invoices)
    
    invoice_data = list(invoices.values("id", "invoice_number", "client__name"))
    print(invoice_data)
    
    return JsonResponse({"invoices": invoice_data})

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
def clientForm(request):
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
    if client.assigned_to != request.user:
        return HttpResponseRedirect(reverse("invoices:clients"))
    else:
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
    if client.assigned_to != request.user:
        return HttpResponseRedirect(reverse("invoices:clients"))
    else:
        if request.method == "POST":
            client.delete()
            return HttpResponseRedirect(reverse("invoices:clients"))
        return render(request, "invoices/clientDetail.html", {"client": client})
    
# Filter Clients
@login_required()
def filterClients(request):
    query = request.GET.get("query", "").strip()
    print(query)
    if not query: 
        clients = Client.objects.filter(assigned_to=request.user)
    else: 
        clients = Client.objects.filter(
            Q(assigned_to=request.user) & (
                Q(name__icontains=query) |
                Q(nip_number__icontains=query)
            )
        )
    
    client_data = list(clients.values("id", "name", "nip_number"))
    
    return JsonResponse({"clients": client_data})

# Get one Client
@login_required()
def getClient(request, client_id):
    client = list(Client.objects.filter(
            Q(assigned_to=request.user) & Q(id__icontains=client_id)
        ).values("id", "name", "nip_number", "street", "city", "postal_code"))
    print(client)
    return JsonResponse({"client": client})

# Products
@login_required()
def products(request):
    all_products = Product.objects.filter(assigned_to=request.user)
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
            product = form.save(commit=False)
            product.assigned_to = request.user
            product = form.save()
            form.save()
            return HttpResponseRedirect(reverse("invoices:products"))
    else:
        form = ProductForm()

    return render(request, "invoices/productForm.html", {"form": form})

# Product Detail
@login_required()
def productDetail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if product.assigned_to != request.user:
        return HttpResponseRedirect(reverse("invoices:products"))
    else:
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
    if product.assigned_to != request.user:
        return HttpResponseRedirect(reverse("invoices:products"))
    else:
        if request.method == "POST":
            product.delete()
            return HttpResponseRedirect(reverse("invoices:products"))
        return render(request, "invoices/productDetail.html", {"product": product})

# Filter Products
@login_required()
def filterProducts(request):
    query = request.GET.get("query", "").strip()
    print(query)
    if not query: 
        products = Product.objects.filter(assigned_to=request.user)
    else: 
        products = Product.objects.filter(
            Q(assigned_to=request.user) & (
                Q(name__icontains=query) |
                Q(price_netto__icontains=query)
            )
        )
    
    product_data = list(products.values("id", "name", "price_netto"))
    
    return JsonResponse({"products": product_data})

# Get Products
@login_required()
def getProducts(request):
    products = list(Product.objects.filter(assigned_to=request.user).values("id", "name", "price_netto", "tax"))
    print(products)
    return JsonResponse({"products": products})
