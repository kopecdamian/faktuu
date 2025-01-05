from django.urls import path

from . import views

urlpatterns = [
    # /invoices
    path("invoices/", views.index, name="index"),
    # /invoice/5
    path("invoices/<int:invoice_id>/", views.detail, name="detail"),
    # /invoice/5/pdf
    path("invoices/<int:invoice_id>/pdf/", views.pdf, name="products")
]