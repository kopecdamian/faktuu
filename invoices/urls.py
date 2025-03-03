from django.urls import path

from . import views

app_name = "invoices"
urlpatterns = [
    # /invoices
    path("", views.invoices, name="invoices"),
    # /invoice/create
    path("create", views.invoiceCreate, name="invoiceCreate"),
    # /invoice/5
    path("<int:invoice_id>/", views.invoiceDetail, name="invoiceDetail"),
     # /invoice/invoices/5/delete
    path("invoices/<int:invoice_id>/delete", views.invoiceDelete, name="invoiceDelete"),
    # /invoice/5/pdf
    path("<int:invoice_id>/pdf/", views.generateInvoicePdf, name="generateInvoicePdf"),

    # /invoice/clients
    path("clients", views.clients, name="clients"),
    # /invoice/clients/create
    path("clients/create", views.clientForm, name="clientForm"),
    # /invoice/clients/5
    path("clients/<int:client_id>/", views.clientDetail, name="clientDetail"),
    # /invoice/clients/5/delete
    path("clients/<int:client_id>/delete", views.clientDelete, name="clientDelete"),

    # /invoice/products
    path("products", views.products, name="products"),
    # /invoice/products/create
    path("products/create", views.productForm, name="productForm"),
    # /invoice/products/5
    path("products/<int:product_id>/", views.productDetail, name="productDetail"),
    # /invoice/products/5/delete
    path("products/<int:product_id>/delete", views.productDelete, name="productDelete"),
]