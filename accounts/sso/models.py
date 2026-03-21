# https://docs.djangoproject.com/en/6.0/intro/tutorial02/#creating-models
from django.db import models
from django.contrib.auth.models import User


class SsoUser(models.Model):
    PROVIDER_GITHUB = "GITHUB"
    PROVIDER_CHOICES = [
        (PROVIDER_GITHUB, "Github"),
    ]

    provider = models.CharField(
        max_length=max((len(x[0]) for x in PROVIDER_CHOICES)),
        choices=PROVIDER_CHOICES,
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    sub = models.CharField(
        max_length=64,
    )
