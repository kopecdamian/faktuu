from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    path("signup/", views.signUp, name="signup"),
    path("account-settings/", views.accountSettings, name="accountSettings"),
    path("activate/<uidb64>/<token>/", views.activate, name="activate"),
]