from django.urls import path
from core.views import (
    AssignDoctorView,
    DoctorConsultationView,
    MedicalHistoryListView,
    MedicalHistoryDetailView,
    TestAPIView,
    CompleteTestAPIView,
    PatientListView,
    PatientDetailView,
    TestListView,
    TestDetailView,
    AssignTestsView,
    RecordTestResultView,
    PrescriptionListView,
    PrescriptionDetailView,
    DispenseMedicinesView,
    AddPrescriptionView,
    VisitListView,
    VisitDetailView,
    CompleteVisitView,
)


urlpatterns = [
    # Patient list and create view
    path("patients/", PatientListView.as_view(), name="patient_list"),
    # Patient detail view for retrieve, update, and delete
    path("patients/<int:pk>/", PatientDetailView.as_view(), name="patient_detail"),
    # URL to list all visits or create a new visit
    path("visits/", VisitListView.as_view(), name="visit-list"),
    path("visits/<int:visit_id>/", VisitDetailView.as_view(), name="visit-detail"),
    # Visits and Assign Doctor
    path(
        "visits/assign-doctor/",
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
    # URL for assigning tests to a patient during a visit
    path("tests/assign-tests/", AssignTestsView.as_view(), name="assign_tests"),
    # URL for recording test results
    path(
        "tests/record-test-result/",
        RecordTestResultView.as_view(),
        name="record_test_result",
    ),
    # Prescriptions
    path("prescriptions/", PrescriptionListView.as_view(), name="prescription_list"),
    path(
        "prescriptions/<int:pk>/",
        PrescriptionDetailView.as_view(),
        name="prescription_detail",
    ),
    # Dispense Medicines URL
    path(
        "dispense-medicines/",
        DispenseMedicinesView.as_view(),
        name="dispense-medicines",
    ),
    # Add Prescription URL
    path("add-prescription/", AddPrescriptionView.as_view(), name="add-prescription"),
    # Invoices
    path("complete-visit/", CompleteVisitView.as_view(), name="complete-visit"),
]
