from django.urls import path
from core.management_views import (
    ItemTypeListView, ItemTypeDetailView,
    InsuranceListView, InsuranceDetailView,
    HospitalItemListView, HospitalItemDetailView, HospitalBulkUploadView,
    InsuranceCompanyListView, InsuranceCompanyDetailView
)

urlpatterns = [
    # Insurance URLs
    path('insurance/', InsuranceListView.as_view(), name='insurance-list'),
    path('insurance/<int:pk>/', InsuranceDetailView.as_view(), name='insurance-detail'),

    # Hospital Item URLs
    path('hospital-items/', HospitalItemListView.as_view(), name='hospital-item-list'),
    path('hospital-items/<int:pk>/', HospitalItemDetailView.as_view(), name='hospital-item-detail'),
    path("hospital-items/bulk-upload/", HospitalBulkUploadView.as_view(), name="hospital-item-bulk-upload"),

    # Item type URLs
    path('item-types/', ItemTypeListView.as_view(), name='item-type-list'),
    path('item-types/<int:pk>/', ItemTypeDetailView.as_view(), name='item-type-detail'),

    # Insurance Company URLs
    path('insurance-companies/', InsuranceCompanyListView.as_view(), name='insurance-company-list'),
    path('insurance-companies/<int:pk>/', InsuranceCompanyDetailView.as_view(), name='insurance-company-detail'),
]
