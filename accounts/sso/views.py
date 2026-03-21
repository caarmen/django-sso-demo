# https://docs.authlib.org/en/stable/client/frameworks.html#frameworks-clients
import logging

from authlib.integrations.django_client import OAuth
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import login

from accounts.sso.models import SsoUser

logger = logging.getLogger(__name__)


def github_authorize(request):
    oauth = OAuth()
    oauth.register("github")
    # https://docs.authlib.org/en/stable/client/django.html#routes-for-authorization
    redirect_uri = request.build_absolute_uri(reverse("accounts:github_callback"))
    resp = oauth.github.authorize_redirect(request, redirect_uri)
    return resp


def github_callback(request):
    oauth = OAuth()
    oauth.register("github")
    token = oauth.github.authorize_access_token(request)
    resp = oauth.github.get("user", token=token)
    resp.raise_for_status()
    provider_user = resp.json()
    logger.debug(f"Fetched user {provider_user}")
    sub = provider_user["id"]

    # See if the user already logged in here before.
    try:
        provider_user = SsoUser.objects.get(
            provider=SsoUser.PROVIDER_GITHUB,
            sub=sub,
        )
    except SsoUser.DoesNotExist:
        # The user hasn't logged in with Github before.
        resp = oauth.github.get("user/emails", token=token)
        resp.raise_for_status()
        provider_user_emails = resp.json()
        primary_email_data = next(
            x for x in provider_user_emails if x["primary"] is True
        )
        email = primary_email_data["email"]

        # See if we find a matching user for this user's email.
        # If not, create it.
        user, created = User.objects.get_or_create(
            defaults={
                "email": email,
                "username": provider_user["login"],
                "first_name": provider_user["login"],
            },
            email=email,
        )

        # Create an entry for their Github login.
        provider_user = SsoUser.objects.create(
            user=user,
            provider=SsoUser.PROVIDER_GITHUB,
            sub=sub,
        )

    login(request, provider_user.user)

    response = redirect(to=reverse("accounts:home"))
    return response
