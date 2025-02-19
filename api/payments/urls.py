from django.urls import path
from core.payment_views import (
    ConsultationPaymentView,
    GenerateTestPaymentView,
    GeneratePrescriptionPaymentView,
    CompletePaymentView,
    PaymentListView,
    PaymentDetailView,
    PaymentItemListView,
    PaymentItemDetailView,
    InvoiceListView,
    InvoiceDetailView,
    InvoiceItemListView,
    InvoiceItemDetailView,
    SubmitToInsuranceView,
    VisitPaymentDetailView,
    VisitPaymentItemListView,
)

urlpatterns = []


urlpatterns = [
    path("", PaymentListView.as_view(), name="payment_list"),
    path("<int:pk>/", PaymentDetailView.as_view(), name="payment_detail"),
    path("payment-items/", PaymentItemListView.as_view(), name="payment-item-list"),
    path(
        "payment-items/<int:pk>/",
        PaymentItemDetailView.as_view(),
        name="payment-item-detail",
    ),
    path(
        "visits/<int:visit_id>/payments/",
        VisitPaymentDetailView.as_view(),
        name="visit-payment-detail",
    ),
    path(
        "visits/<int:visit_id>/payment-items/",
        VisitPaymentItemListView.as_view(),
        name="visit-payment-item-list",
    ),
    path("invoices/", InvoiceListView.as_view(), name="invoice_list"),
    path("invoices/<int:pk>/", InvoiceDetailView.as_view(), name="invoice_detail"),
    path("invoice-items/", InvoiceItemListView.as_view(), name="invoice-item-list"),
    path(
        "invoice-items/<int:pk>/",
        InvoiceItemDetailView.as_view(),
        name="invoice-item-detail",
    ),
    path(
        "generate-consultation-payment/",
        ConsultationPaymentView.as_view(),
        name="generate-consultation-payment",
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
        "visits/<int:visit_id>/complete-payment/",
        CompletePaymentView.as_view(),
        name="complete-payment",
    ),
    path(
        "submit-to-insurance/",
        SubmitToInsuranceView.as_view(),
        name="submit-to-insurance",
    ),
]
