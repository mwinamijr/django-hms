from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import PatientViewSet, VisitViewSet, PaymentViewSet, VitalsViewSet

router = DefaultRouter()
router.register(r"patients", PatientViewSet)
router.register(r"visits", VisitViewSet)
router.register(r"payments", PaymentViewSet)
router.register(r"vitals", VitalsViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
