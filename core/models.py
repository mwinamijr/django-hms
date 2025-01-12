from django.db import models
from django.conf import settings
from users.models import Department


class Patient(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    payment_method = models.CharField(
        max_length=50,
        choices=[
            ("cash", "Cash"),
            ("insurance", "Insurance"),
        ],
    )
    insurance_details = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Visit(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    visit_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Visit for {self.patient} to {self.department}"


class Payment(models.Model):
    visit = models.OneToOneField(Visit, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("completed", "Completed"),
        ],
        default="pending",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for {self.visit} - {self.status}"


class Vitals(models.Model):
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    temperature = models.DecimalField(
        max_digits=4, decimal_places=1, null=True, blank=True
    )
    blood_pressure = models.CharField(max_length=20, null=True, blank=True)
    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Vitals for {self.visit}"
