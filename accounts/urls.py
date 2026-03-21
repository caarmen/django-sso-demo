# https://docs.djangoproject.com/en/6.0/intro/tutorial01/#write-your-first-view

from django.urls import path

from . import views
from accounts.sso import views as sso_views

app_name = "accounts"
urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("sso/github/authorize/", sso_views.github_authorize, name="github_authorize"),
    path("sso/github/callback/", sso_views.github_callback, name="github_callback"),
]
