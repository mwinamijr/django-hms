from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Visit, MedicalHistory, Test, Patient, Prescription, Invoice
from .serializers import (
    VisitSerializer,
    MedicalHistorySerializer,
    TestSerializer,
    PrescriptionSerializer,
    PatientSerializer,
    InvoiceSerializer,
)


class PatientListView(APIView):
    """
    Handles GET and POST requests for the list of patients.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieve a list of all patients.
        """
        patients = Patient.objects.all()
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create a new patient record.
        """
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatientDetailView(APIView):
    """
    Handles GET, PUT, PATCH, and DELETE requests for a single patient.
    """

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Patient, pk=pk)

    def get(self, request, pk):
        """
        Retrieve details of a specific patient.
        """
        patient = self.get_object(pk)
        serializer = PatientSerializer(patient)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """
        Update an entire patient record.
        """
        patient = self.get_object(pk)
        serializer = PatientSerializer(patient, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        """
        Partially update a patient record.
        """
        patient = self.get_object(pk)
        serializer = PatientSerializer(patient, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete a patient record.
        """
        patient = self.get_object(pk)
        patient.delete()
        return Response(
            {"detail": "Patient record deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


# --- Visit Management ---
class AssignDoctorAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, visit_id):
        try:
            visit = Visit.objects.get(pk=visit_id)
            doctor_id = request.data.get("doctor_id")
            visit.doctor_id = doctor_id
            visit.save()
            return Response(
                {"status": "Doctor assigned successfully"}, status=status.HTTP_200_OK
            )
        except Visit.DoesNotExist:
            return Response(
                {"error": "Visit not found"}, status=status.HTTP_404_NOT_FOUND
            )


# --- Medical History ---
class MedicalHistoryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, visit_id):
        histories = MedicalHistory.objects.filter(visit_id=visit_id)
        serializer = MedicalHistorySerializer(histories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MedicalHistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MedicalHistoryListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        histories = MedicalHistory.objects.all()
        serializer = MedicalHistorySerializer(histories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = MedicalHistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MedicalHistoryDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(MedicalHistory, pk=pk)

    def get(self, request, pk):
        history = self.get_object(pk)
        serializer = MedicalHistorySerializer(history)
        return Response(serializer.data, status=status.HTTP_200_OK)


# --- Test Management ---
class TestAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, visit_id):
        tests = Test.objects.filter(visit_id=visit_id)
        serializer = TestSerializer(tests, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompleteTestAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, test_id):
        try:
            test = Test.objects.get(pk=test_id)
            test.result = request.data.get("result")
            test.is_completed = True
            test.conducted_by = request.user
            test.save()
            return Response(
                {"status": "Test completed successfully"}, status=status.HTTP_200_OK
            )
        except Test.DoesNotExist:
            return Response(
                {"error": "Test not found"}, status=status.HTTP_404_NOT_FOUND
            )


# Test Views
class TestListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tests = Test.objects.all()
        serializer = TestSerializer(tests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TestDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Test, pk=pk)

    def get(self, request, pk):
        test = self.get_object(pk)
        serializer = TestSerializer(test)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        test = self.get_object(pk)
        serializer = TestSerializer(test, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# --- Prescription Management ---
class PrescriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, visit_id):
        prescriptions = Prescription.objects.filter(visit_id=visit_id)
        serializer = PrescriptionSerializer(prescriptions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PrescriptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Prescription Views
class PrescriptionListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        prescriptions = Prescription.objects.all()
        serializer = PrescriptionSerializer(prescriptions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PrescriptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PrescriptionDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Prescription, pk=pk)

    def get(self, request, pk):
        prescription = self.get_object(pk)
        serializer = PrescriptionSerializer(prescription)
        return Response(serializer.data, status=status.HTTP_200_OK)


# --- Invoice Management ---
class InvoiceAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, visit_id):
        try:
            invoice = Invoice.objects.get(visit_id=visit_id)
            serializer = InvoiceSerializer(invoice)
            return Response(serializer.data)
        except Invoice.DoesNotExist:
            return Response(
                {"error": "Invoice not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def post(self, request):
        serializer = InvoiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PayInvoiceAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, invoice_id):
        try:
            invoice = Invoice.objects.get(pk=invoice_id)
            invoice.is_paid = True
            invoice.save()
            return Response(
                {"status": "Invoice paid successfully"}, status=status.HTTP_200_OK
            )
        except Invoice.DoesNotExist:
            return Response(
                {"error": "Invoice not found"}, status=status.HTTP_404_NOT_FOUND
            )


# Invoice Views
class InvoiceListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        invoices = Invoice.objects.all()
        serializer = InvoiceSerializer(invoices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = InvoiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InvoiceDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Invoice, pk=pk)

    def get(self, request, pk):
        invoice = self.get_object(pk)
        serializer = InvoiceSerializer(invoice)
        return Response(serializer.data, status=status.HTTP_200_OK)
