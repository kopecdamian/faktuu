from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# Invoices
def index(request):
    return HttpResponse("Invoices page.")

# Detail
def detail(request, invoice_id):
    return HttpResponse("Invoice detail page.")

def pdf(request, invoice_id):
    return HttpResponse("Invoice download page.")