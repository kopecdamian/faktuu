from django.urls import path

from . import views

app_name = "invoices"
urlpatterns = [
    # /invoices
    path("invoices/", views.invoices, name="invoices"),
    # /invoice/create
    path("invoices/create", views.invoiceForm, name="invoiceForm"),
    # /invoice/save
    # path("invoices/save", views.save, name="save"),
    # /invoice/5
    path("invoices/<int:invoice_id>/", views.invoiceDetail, name="invoiceDetail"),
     # /invoice/invoices/5/delete
    path("invoices/invoices/<int:invoice_id>/delete", views.invoiceDelete, name="invoiceDelete"),
    # /invoice/5/pdf
    path("invoices/<int:invoice_id>/pdf/", views.pdf, name="products"),

    # /invoice/clients
    path("invoices/clients", views.clients, name="clients"),
    # /invoice/clients/create
    path("invoices/clients/create", views.clientform, name="clientform"),
    # /invoice/clients/save
    # path("invoices/clients/save", views.saveclient, name="saveclient"),
    # /invoice/clients/5
    path("invoices/clients/<int:client_id>/", views.clientDetail, name="clientDetail"),
    # /invoice/clients/5/delete
    path("invoices/clients/<int:client_id>/delete", views.clientDelete, name="clientDelete"),

    # /invoice/products
    path("invoices/products", views.products, name="products"),
    # /invoice/products/create
    path("invoices/products/create", views.productForm, name="productForm"),
    # /invoice/products/save
    # path("invoices/products/save", views.productSave, name="productSave"),
    # /invoice/products/5
    path("invoices/products/<int:product_id>/", views.productDetail, name="productDetail"),
    # /invoice/products/5/delete
    path("invoices/products/<int:product_id>/delete", views.productDelete, name="productDelete"),
]