from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .managers import CustomUserManager


class Department(models.Model):
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=10)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="first name"
    )
    middle_name = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="middle name"
    )
    last_name = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="last name"
    )
    email = models.EmailField(_("email address"), unique=True)
    date_joined = models.DateTimeField(default=timezone.now)

    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, blank=True
    )
    role = models.CharField(
        max_length=50,
        choices=[
            ("doctor", "Doctor"),
            ("nurse", "Nurse"),
            ("receptionist", "Receptionist"),
            ("cashier", "Cashier"),
            ("lab_technician", "Lab Technician"),
            ("radiology_staff", "Radiology Staff"),
            ("pharmacist", "Pharmacist"),
            ("admin", "Admin"),
        ],
    )

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        # get prefix for email and use that as username
        # username = (self.email).
        return f"{self.email} ({self.role})"
