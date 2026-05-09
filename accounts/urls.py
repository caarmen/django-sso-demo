# https://docs.djangoproject.com/en/6.0/intro/tutorial01/#write-your-first-view

from django.urls import path

from . import views

app_name = "accounts"
urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login, name="login"),
]
