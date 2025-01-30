from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Invoice, InvoiceCounter
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
    return render(request, "invoices/forms.html")

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
            client = client,
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