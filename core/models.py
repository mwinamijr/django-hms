from datetime import datetime
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from users.models import Department


def validate_dob(value):
    if value > now().date():
        raise ValidationError("Date of birth cannot be in the future.")


class InsuranceCompany(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=12, blank=True, null=True)
    description = models.TextField(
        blank=True, null=True
    )  # Optional field for additional details
    created_at = models.DateTimeField(
        auto_now_add=True
    )  # Timestamp when the company is added
    updated_at = models.DateTimeField(
        auto_now=True
    )  # Timestamp when the company info is updated

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Insurance Company"
        verbose_name_plural = "Insurance Companies"


class ItemType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(
        blank=True, null=True
    )  # Optional field for additional details
    created_at = models.DateTimeField(
        auto_now_add=True
    )  # Timestamp when the company is added
    updated_at = models.DateTimeField(
        auto_now=True
    )  # Timestamp when the company info is updated

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Item Type"
        verbose_name_plural = "Item Types"


class HospitalItem(models.Model):
    name = models.CharField(
        max_length=255
    )  # Name of the item (e.g., "Blood Test", "Aspirin", "Consultation")
    description = models.TextField(
        blank=True, null=True
    )  # Optional description of the item
    item_type = models.ForeignKey(
        ItemType, on_delete=models.SET_NULL, blank=True, null=True
    )  # Type of the item
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price of the item
    is_active = models.BooleanField(
        default=True
    )  # Whether the item is currently active and available
    created_at = models.DateTimeField(
        auto_now_add=True
    )  # Timestamp when the item is added
    updated_at = models.DateTimeField(
        auto_now=True
    )  # Timestamp for last update to the item

    # Many-to-many relationship with InsuranceCompany
    insurance_companies = models.ManyToManyField(
        InsuranceCompany, related_name="covered_items", blank=True
    )

    def __str__(self):
        return f"{self.name} - {self.price}"

    class Meta:
        verbose_name = "Hospital Item"
        verbose_name_plural = "Hospital Items"


class Patient(models.Model):
    patient_number = models.CharField(
        max_length=9, unique=True, blank=True, null=True, db_index=True
    )
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(unique=True, db_index=True, max_length=15)
    address = models.TextField()
    registration_date = models.DateField(auto_now_add=True, null=True, blank=True)
    occupation = models.CharField(max_length=50, null=True, blank=True)
    kin_name = models.CharField(max_length=200, null=True, blank=True)
    kin_relation = models.CharField(max_length=50, null=True, blank=True)
    kin_phone = models.CharField(max_length=200, null=True, blank=True)
    national_id = models.CharField(max_length=50, null=True, blank=True)
    marital_status = models.CharField(
        max_length=50,
        choices=[("single", "Single"), ("married", "Married")],
        default="single",
    )
    gender = models.CharField(
        max_length=10,
        choices=[("male", "Male"), ("female", "Female")],
        blank=True,
        null=True,
    )
    priority = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("patient_number",)

    def save(self, *args, **kwargs):
        if not self.patient_number:
            today_str = datetime.today().strftime("%d%m%y")
            last_patient = (
                Patient.objects.filter(patient_number__startswith=today_str)
                .order_by("-id")
                .first()
            )
            new_number = (
                int(last_patient.patient_number[-3:]) + 1 if last_patient else 1
            )
            self.patient_number = f"{today_str}{new_number:03d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.patient_number})"

    @property
    def payment_method(self):
        return "insurance" if hasattr(self, "insurance") else "cash"


class Insurance(models.Model):
    patient = models.OneToOneField(
        Patient, on_delete=models.CASCADE, related_name="insurance"
    )
    provider = models.ForeignKey(
        InsuranceCompany, on_delete=models.CASCADE
    )  # Link to the InsuranceCompany model
    policy_number = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.patient.first_name} {self.patient.last_name} - {self.provider.name} - {self.policy_number}"


class Visit(models.Model):
    visit_number = models.CharField(
        max_length=9, unique=True, blank=True, null=True, db_index=True
    )
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="visits"
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        related_name="visits",
        null=True,
        blank=True,
    )
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
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_visits",
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("onprogress", "On Progress"),
            ("completed", "Completed"),
        ],
        default="pending",
    )
    visit_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Visit for {self.patient} to {self.department}"

    def save(self, *args, **kwargs):
        if Visit.objects.filter(
            patient=self.patient,
            department=self.department,
            visit_date=datetime.today(),
        ).exists():
            raise ValidationError(
                "Patient already has a visit to this department today."
            )

        if not self.visit_number:
            today_str = datetime.today().strftime("%d%m%y")
            last_visit = (
                Visit.objects.filter(visit_number__startswith=today_str)
                .order_by("-id")
                .first()
            )
            new_number = int(last_visit.visit_number[-3:]) + 1 if last_visit else 1
            self.visit_number = f"{today_str}{new_number:03d}"

        super().save(*args, **kwargs)


class VisitComment(models.Model):
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE, related_name="comments")
    description = models.TextField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.created_by} on {self.visit.visit_number} - {self.visit.patient.first_name} {self.visit.patient.last_name} "


class Payment(models.Model):
    """
    This is used to track the total amount of payments in the entire visit
    """

    visit = models.ForeignKey(Visit, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("completed", "Completed")],
        default="pending",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for {self.visit} - {self.status}"


class PaymentItem(models.Model):
    """
    This is used to track the total amount of payments in the entire visit
    """

    payment = models.ForeignKey(
        "Payment", on_delete=models.CASCADE, related_name="items"
    )
    item = models.ForeignKey(
        HospitalItem, on_delete=models.SET_NULL, blank=True, null=True
    )
    status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("completed", "Completed")],
        default="pending",
    )

    def __str__(self):
        return f"{self.payment.visit.patient.first_name} {self.payment.visit.patient.last_name} - {self.item.name} (${self.item.price})"

    class Meta:
        verbose_name = "Payment Item"
        verbose_name_plural = "Payment Items"


class Vital(models.Model):
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
    """
    Represents tests conducted during a visit (e.g., Blood Test, X-ray)
    """

    visit = models.ForeignKey("Visit", on_delete=models.CASCADE, related_name="tests")
    item = models.ForeignKey(
        HospitalItem, on_delete=models.CASCADE, blank=True, null=True
    )  # Use HospitalItem
    status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("completed", "Completed")],
        default="pending",
    )

    def __str__(self):
        return f"{self.item.name} - {self.status}"

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
    """
    Represents individual items within an invoice.
    """

    invoice = models.ForeignKey(
        "Invoice", on_delete=models.CASCADE, related_name="items"
    )
    item = models.ForeignKey(
        HospitalItem, on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return f"{self.invoice.visit.patient.first_name} {self.invoice.visit.patient.last_name} - {self.item.name} (${self.item.price})"
