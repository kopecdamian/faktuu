from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.urls import reverse
from django.http import HttpResponse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
import environ
import os

User = get_user_model()

# Get data from file .env
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# user registration
def signUp(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # user account is inactive
            user.save()

            # generating activation token and UID
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            activation_link = request.build_absolute_uri(reverse('activate', kwargs={'uidb64': uid, 'token': token}))

            # sending activation email
            send_mail(
                "Aktywacja konta Faktuu",
                f"Cześć {user.username}, kliknij w link, aby aktywować konto: {activation_link}",
                env("EMAIL_HOST_USER"),
                [user.email],
                fail_silently=False,
            )

            # information about the successful sending of the email
            return render(request, "registration/confirmation_sent.html")

    else:
        form = CustomUserCreationForm()
    
    return render(request, "registration/signup.html", {"form": form})

# user account activation
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect("login") 
    else:
        return HttpResponse("Nieprawidłowy link aktywacyjny", status=400)