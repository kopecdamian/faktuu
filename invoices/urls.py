from django.urls import path

from . import views

app_name = "invoices"
urlpatterns = [
    # /invoices
    path("", views.invoices, name="invoices"),
    # /invoices/create
    path("create", views.invoiceCreate, name="invoiceCreate"),
    # /invoices/5
    path("<int:invoice_id>/", views.invoiceDetail, name="invoiceDetail"),
     # /invoices/invoices/5/delete
    path("invoices/<int:invoice_id>/delete", views.invoiceDelete, name="invoiceDelete"),
    # /invoices/5/pdf
    path("<int:invoice_id>/pdf/", views.generateInvoicePdf, name="generateInvoicePdf"),

    # /invoices/clients
    path("clients", views.clients, name="clients"),
    # /invoices/clients/create
    path("clients/create", views.clientForm, name="clientForm"),
    # /invoice/clients/5
    path("clients/<int:client_id>/", views.clientDetail, name="clientDetail"),
    # /invoice/clients/5/delete
    path("clients/<int:client_id>/delete", views.clientDelete, name="clientDelete"),

    # /invoices/products
    path("products", views.products, name="products"),
    # /invoices/products/create
    path("products/create", views.productForm, name="productForm"),
    # /invoices/products/5
    path("products/<int:product_id>/", views.productDetail, name="productDetail"),
    # /invoices/products/5/delete
    path("products/<int:product_id>/delete", views.productDelete, name="productDelete"),
    # /invoices/products/filter-products
    path("products/filter-products/", views.filterProducts, name="filterProducts"),
]