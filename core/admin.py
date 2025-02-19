from django.contrib import admin
from .models import (
    Patient,
    Payment,
    PaymentItem,
    Visit,
    Vital,
    MedicalHistory,
    Test,
    TestResult,
    Prescription,
    Invoice,
    InvoiceItem,
    Insurance,
    InsuranceCompany,
    HospitalItem,
    ItemType,
    VisitComment,
)

admin.site.register(Patient)
admin.site.register(Visit)
admin.site.register(Vital)
admin.site.register(MedicalHistory)
admin.site.register(Test)
admin.site.register(TestResult)
admin.site.register(Prescription)
admin.site.register(Invoice)
admin.site.register(InvoiceItem)
admin.site.register(Payment)
admin.site.register(PaymentItem)
admin.site.register(InsuranceCompany)
admin.site.register(HospitalItem)
admin.site.register(Insurance)
admin.site.register(ItemType)
admin.site.register(VisitComment)
