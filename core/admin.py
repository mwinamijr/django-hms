from django.contrib import admin
from .models import (
    Patient,
    Payment,
    PaymentItem,
    Visit,
    Vitals,
    MedicalHistory,
    Test,
    TestResult,
    Prescription,
    Invoice,
    InvoiceItem,
)

admin.site.register(Patient)
admin.site.register(Visit)
admin.site.register(Vitals)
admin.site.register(MedicalHistory)
admin.site.register(Test)
admin.site.register(TestResult)
admin.site.register(Prescription)
admin.site.register(Invoice)
admin.site.register(InvoiceItem)
admin.site.register(Payment)
admin.site.register(PaymentItem)
