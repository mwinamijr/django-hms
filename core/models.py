from django.db import models
from django.conf import settings
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
    )
    insurance_details = models.TextField(null=True, blank=True)

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
    visit_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Visit for {self.patient} to {self.department}"


class Payment(models.Model):
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE)
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
    visit = models.ForeignKey("Visit", on_delete=models.CASCADE)
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History for {self.visit.patient} by {self.doctor}"


class Test(models.Model):
    visit = models.ForeignKey("Visit", on_delete=models.CASCADE)
    test_type = models.CharField(max_length=100)
    result = models.TextField(null=True, blank=True)
    conducted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.test_type} for {self.visit}"


class Prescription(models.Model):
    visit = models.ForeignKey("Visit", on_delete=models.CASCADE)
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    medicines = models.TextField()  # e.g., "Paracetamol 500mg x3, Ibuprofen 400mg x2"
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prescription for {self.visit.patient}"


class Invoice(models.Model):
    invoice_number = models.CharField(max_length=50, unique=True)
    visit = models.OneToOneField("Visit", on_delete=models.CASCADE)
    payments = models.ManyToManyField(Payment, related_name="invoices")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Invoice for {self.visit.patient}"


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
