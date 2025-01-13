from django.urls import path
from core.payment_views import (
    ConsultationPaymentView,
    GenerateTestPaymentView,
    GeneratePrescriptionPaymentView,
    CompletePaymentView,
    InvoiceListView,
    InvoiceDetailView,
    SubmitToInsuranceView,
)


urlpatterns = [
    path("invoices/", InvoiceListView.as_view(), name="invoice_list"),
    path("invoices/<int:pk>/", InvoiceDetailView.as_view(), name="invoice_detail"),
    path(
        "generate-consultation-invoice/",
        ConsultationPaymentView.as_view(),
        name="generate-consultation-invoice",
    ),
    path(
        "generate-test-invoice/",
        GenerateTestPaymentView.as_view(),
        name="generate-test-invoice",
    ),
    path(
        "generate-prescription-invoice/",
        GeneratePrescriptionPaymentView.as_view(),
        name="generate-prescription-invoice",
    ),
    path(
        "payment/complete-payment",
        CompletePaymentView.as_view(),
        name="complete-payment",
    ),
    path(
        "submit-to-insurance/",
        SubmitToInsuranceView.as_view(),
        name="submit-to-insurance",
    ),
]
