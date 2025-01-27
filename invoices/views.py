from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Invoice
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
        
        client = request.POST.get('client')
        product = request.POST.get('product')
        
        Invoice.objects.create(
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
    
    # year = datetime.now().year
    # month = datetime.now().month
    # print(Invoice.objects.filter(invoice_number__icontains=f"{year}/{month:02}"))
    return HttpResponse("Invoice download page.")