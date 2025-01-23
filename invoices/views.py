from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.http import HttpResponse
from .models import Invoice

# Create your views here.
# Invoices
def index(request):
    all_invoices = Invoice.objects.all()
    context = {
        "all_invoices": all_invoices,
    }
    return render(request, "invoices/index.html", context)
    

# Detail
def detail(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    return render(request, "invoices/detail.html", {"invoice": invoice})

# PDF
def pdf(request, invoice_id):
    return HttpResponse("Invoice download page.")