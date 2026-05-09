from django.shortcuts import redirect, render

# https://docs.djangoproject.com/en/6.0/topics/auth/default/#auth-web-requests
from django.contrib.auth.decorators import login_required
from django.urls import reverse


@login_required
def home(request):
    return render(request, "accounts/home.html")


def login(request):
    if request.user and request.user.is_authenticated:
        return redirect(to=reverse("accounts:home"))
    return render(request, "accounts/login.html")
