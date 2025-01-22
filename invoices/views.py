from django.shortcuts import render
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
    return HttpResponse("Invoice detail page.")

# PDF
def pdf(request, invoice_id):
    return HttpResponse("Invoice download page.")