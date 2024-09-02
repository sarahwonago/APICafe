from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    Defines the custom user model with added attributes.
    """

    CUSTOMER = 'customer'
    ADMIN = 'admin'
    ROLE_CHOICES = [
        (CUSTOMER, 'Customer'),
        (ADMIN, 'Admin'),
    ]

    role = models.CharField(max_length=200, default=CUSTOMER, choices=ROLE_CHOICES)

    def __str__(self) -> str:
        return self.username