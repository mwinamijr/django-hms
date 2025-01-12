from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Patient, Visit, Payment, Vitals
from .serializers import (
    PatientSerializer,
    VisitSerializer,
    PaymentSerializer,
    VitalsSerializer,
)
from rest_framework.permissions import IsAuthenticated


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]


class VisitViewSet(viewsets.ModelViewSet):
    queryset = Visit.objects.all()
    serializer_class = VisitSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["post"])
    def assign_department(self, request, pk=None):
        visit = self.get_object()
        department_id = request.data.get("department_id")
        visit.department_id = department_id
        visit.save()
        return Response({"status": "department assigned"})


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["post"])
    def pay(self, request, pk=None):
        payment = self.get_object()
        payment.status = "completed"
        payment.save()
        return Response({"status": "payment completed"})


class VitalsViewSet(viewsets.ModelViewSet):
    queryset = Vitals.objects.all()
    serializer_class = VitalsSerializer
    permission_classes = [IsAuthenticated]
