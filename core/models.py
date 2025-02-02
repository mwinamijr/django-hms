from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from users.models import Department


class Patient(models.Model):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
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
        default="cash",
    )
    insurance_provider = models.CharField(max_length=100, null=True, blank=True)
    insurance_policy_number = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Visit(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    assigned_doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_visits",
    )
    status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("completed", "Completed")],
        default="pending",
    )
    visit_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Visit for {self.patient} to {self.department}"


class Payment(models.Model):
    visit = models.ForeignKey("Visit", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("completed", "Completed")],
        default="pending",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for {self.visit} - {self.status}"

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"


class PaymentItem(models.Model):
    PAYMENT_TYPE_CHOICES = [
        ("consultation", "Consultation"),
        ("test", "Test"),
        ("prescription", "Prescription"),
    ]

    payment = models.ForeignKey(
        "Payment", on_delete=models.CASCADE, related_name="items"
    )
    description = models.CharField(max_length=255)  # e.g., "Ultrasound", "Paracetamol"
    type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.type.capitalize()} - {self.description} (${self.price})"

    class Meta:
        verbose_name = "Payment Item"
        verbose_name_plural = "Payment Items"


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


class MedicalHistory(models.Model):
    visit = models.ForeignKey(
        "Visit", on_delete=models.CASCADE, related_name="histories"
    )
    patient = models.ForeignKey(
        "Patient", on_delete=models.CASCADE, related_name="histories"
    )
    description = models.TextField()
    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History for {self.patient} - {self.created_at}"

    class Meta:
        verbose_name = "Medical History"
        verbose_name_plural = "Medical Histories"


class Test(models.Model):
    VISIT_TYPES = [
        ("laboratory", "Laboratory"),
        ("radiology", "Radiology"),
    ]

    visit = models.ForeignKey("Visit", on_delete=models.CASCADE, related_name="tests")
    name = models.CharField(max_length=255)  # e.g., "Blood Test", "X-ray"
    type = models.CharField(max_length=50, choices=VISIT_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("completed", "Completed")],
        default="pending",
    )

    def __str__(self):
        return f"{self.name} ({self.type}) - {self.status}"

    class Meta:
        verbose_name = "Test"
        verbose_name_plural = "Tests"


class TestResult(models.Model):
    test = models.OneToOneField("Test", on_delete=models.CASCADE, related_name="result")
    result_details = models.TextField()
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Result for {self.test.name}"

    class Meta:
        verbose_name = "Test Result"
        verbose_name_plural = "Test Results"


class Prescription(models.Model):
    visit = models.ForeignKey(
        Visit, on_delete=models.CASCADE, related_name="prescriptions"
    )
    medicine_name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=100)  # e.g., "1 tablet twice a day"
    quantity = models.IntegerField()  # e.g., 10 tablets
    frequency = models.CharField(max_length=100)  # e.g., "After meals"
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("dispensed", "Dispensed")],
        default="pending",
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )  # Track when prescription is created

    def __str__(self):
        return f"{self.medicine_name} for {self.visit.patient} - {self.dosage} ({self.quantity} pcs)"


class Invoice(models.Model):
    visit = models.OneToOneField("Visit", on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    is_insurance = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice for {self.visit.patient} - Insurance: {self.is_insurance}"

    def clean(self):
        if self.is_insurance:
            if (
                not self.visit.patient.insurance_provider
                or not self.visit.patient.insurance_policy_number
            ):
                raise ValidationError(
                    "Insurance provider and policy number must be provided if insurance is selected."
                )


class InvoiceItem(models.Model):
    INVOICE_TYPE_CHOICES = [
        ("consultation", "Consultation"),
        ("test", "Test"),
        ("prescription", "Prescription"),
    ]

    invoice = models.ForeignKey(
        "Invoice", on_delete=models.CASCADE, related_name="items"
    )
    description = models.CharField(max_length=255)  # e.g., "Ultrasound", "Paracetamol"
    type = models.CharField(max_length=20, choices=INVOICE_TYPE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.type.capitalize()} - {self.description} (${self.price})"
