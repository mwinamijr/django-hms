from django.contrib import admin
from .models import (
    Patient,
    Payment,
    Visit,
    Vitals,
    MedicalHistory,
    Test,
    Prescription,
    Invoice,
)

admin.site.register(Patient)
admin.site.register(Visit)
admin.site.register(Vitals)
admin.site.register(MedicalHistory)
admin.site.register(Test)
admin.site.register(Prescription)
admin.site.register(Invoice)
admin.site.register(Payment)
