from django.urls import path
from core.views import (
    AssignDoctorView,
    DoctorConsultationView,
    MedicalHistoryListView,
    MedicalHistoryDetailView,
    TestAPIView,
    CompleteTestAPIView,
    PrescriptionAPIView,
    InvoiceAPIView,
    PayInvoiceAPIView,
    PatientListView,
    PatientDetailView,
    TestListView,
    TestDetailView,
    PrescriptionListView,
    PrescriptionDetailView,
    InvoiceListView,
    InvoiceDetailView,
    VisitListView,
    VisitDetailView,
    CompletePaymentView,
)


urlpatterns = [
    # Patient list and create view
    path("patients/", PatientListView.as_view(), name="patient_list"),
    # Patient detail view for retrieve, update, and delete
    path("patients/<int:pk>/", PatientDetailView.as_view(), name="patient_detail"),
    # URL to list all visits or create a new visit
    path("visits/", VisitListView.as_view(), name="visit-list"),
    path("visit/<int:visit_id>/", VisitDetailView.as_view(), name="visit-detail"),
    # Visits and Assign Doctor
    path(
        "visits/<int:visit_id>/assign-doctor/",
        AssignDoctorView.as_view(),
        name="assign_doctor",
    ),
    # URL to handle doctor's consultation for a patient
    path(
        "api/doctor-consultation/",
        DoctorConsultationView.as_view(),
        name="doctor-consultation",
    ),
    # Medical History
    path(
        "medical-history/",
        MedicalHistoryListView.as_view(),
        name="medical_history_list",
    ),
    path(
        "medical-history/<int:pk>/",
        MedicalHistoryDetailView.as_view(),
        name="medical_history_detail",
    ),
    # Tests
    path("tests/<int:visit_id>/", TestAPIView.as_view(), name="tests"),
    path(
        "tests/<int:test_id>/complete/",
        CompleteTestAPIView.as_view(),
        name="complete_test",
    ),
    path("tests/", TestListView.as_view(), name="test_list"),
    path("tests/<int:pk>/", TestDetailView.as_view(), name="test_detail"),
    # Prescriptions
    path("prescriptions/", PrescriptionListView.as_view(), name="prescription_list"),
    path(
        "prescriptions/<int:pk>/",
        PrescriptionDetailView.as_view(),
        name="prescription_detail",
    ),
    path(
        "prescriptions/<int:visit_id>/",
        PrescriptionAPIView.as_view(),
        name="prescriptions",
    ),
    # Invoices
    path(
        "payment/complete-payment",
        CompletePaymentView.as_view(),
        name="complete-payment",
    ),
    path("invoices/<int:visit_id>/", InvoiceAPIView.as_view(), name="invoice"),
    path(
        "invoices/<int:invoice_id>/pay/",
        PayInvoiceAPIView.as_view(),
        name="pay_invoice",
    ),
    path("invoices/", InvoiceListView.as_view(), name="invoice_list"),
    path("invoices/<int:pk>/", InvoiceDetailView.as_view(), name="invoice_detail"),
]
