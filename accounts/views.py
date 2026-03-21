from django.shortcuts import render

# https://docs.djangoproject.com/en/6.0/topics/auth/default/#auth-web-requests
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    return render(request, "accounts/home.html")
