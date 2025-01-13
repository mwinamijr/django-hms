from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import (
    Visit,
    MedicalHistory,
    Test,
    Patient,
    Prescription,
    Invoice,
    Payment,
    PaymentItem,
)
from users.models import CustomUser as User
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


class VisitListView(APIView):
    """
    View to list all visits or create a new visit.
    """

    def get(self, request):
        visits = Visit.objects.all()  # Get all visits
        serializer = VisitSerializer(visits, many=True)  # Serialize the visits
        return Response(serializer.data)  # Return the data in JSON format

    def post(self, request):
        serializer = VisitSerializer(data=request.data)  # Deserialize the incoming data
        if serializer.is_valid():
            serializer.save()  # Save the new visit
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )  # Return the serialized data with a 201 status
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )  # Return validation errors if any


class VisitDetailView(APIView):
    """
    View to retrieve, update, or delete a specific visit.
    """

    def get_object(self, visit_id):
        try:
            return Visit.objects.get(id=visit_id)
        except Visit.DoesNotExist:
            return None

    def get(self, request, visit_id):
        visit = self.get_object(visit_id)  # Get the specific visit
        if visit is not None:
            serializer = VisitSerializer(visit)
            return Response(serializer.data)  # Return visit data
        return Response(
            {"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND
        )  # Handle if visit doesn't exist

    def put(self, request, visit_id):
        visit = self.get_object(visit_id)
        if visit is not None:
            serializer = VisitSerializer(
                visit, data=request.data, partial=False
            )  # Deserialize and validate the data
            if serializer.is_valid():
                serializer.save()  # Save the updated visit
                return Response(serializer.data)  # Return the updated visit data
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, visit_id):
        visit = self.get_object(visit_id)
        if visit is not None:
            visit.delete()  # Delete the visit
            return Response(
                status=status.HTTP_204_NO_CONTENT
            )  # Return 204 No Content status
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)


class AssignDoctorView(APIView):
    def post(self, request):
        """
        Assign a doctor to the patient's visit and create a consultation fee payment.
        """
        try:
            visit_id = request.data.get("visit_id")
            doctor_id = request.data.get("doctor_id")
            consultation_fee = request.data.get("consultation_fee")

            if not (visit_id and doctor_id and consultation_fee):
                return Response(
                    {"detail": "Missing required fields."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            with transaction.atomic():
                # Fetch the visit and doctor
                visit = Visit.objects.get(id=visit_id)
                doctor = User.objects.get(id=doctor_id, role="doctor")

                # Assign the doctor to the visit
                visit.assigned_doctor = doctor
                visit.save()

                # Create a Payment record if not exists
                payment, created = Payment.objects.get_or_create(visit=visit)

                # Add a PaymentItem for the consultation fee
                PaymentItem.objects.create(
                    payment=payment,
                    description="Consultation Fee",
                    type="consultation",
                    price=consultation_fee,
                )

                return Response(
                    {"detail": "Doctor assigned and consultation fee recorded."},
                    status=status.HTTP_200_OK,
                )
        except Visit.DoesNotExist:
            return Response(
                {"detail": "Visit not found."}, status=status.HTTP_404_NOT_FOUND
            )
        except User.DoesNotExist:
            return Response(
                {"detail": "Doctor not found."}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DoctorConsultationView(APIView):
    def post(self, request):
        """
        Handle the doctor's consultation for a patient.
        """
        try:
            visit_id = request.data.get("visit_id")
            doctor_id = request.data.get("doctor_id")
            new_history = request.data.get("new_history")

            # Validate if all required fields are provided
            if not all([visit_id, doctor_id, new_history]):
                return Response(
                    {
                        "detail": "Missing required fields: visit_id, doctor_id, and new_history are required."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Fetch the visit and ensure the doctor is assigned to it
            try:
                visit = Visit.objects.get(id=visit_id)
            except Visit.DoesNotExist:
                return Response(
                    {"detail": "Visit not found."}, status=status.HTTP_404_NOT_FOUND
                )

            try:
                doctor = User.objects.get(id=doctor_id, role="doctor")
            except User.DoesNotExist:
                return Response(
                    {"detail": "Doctor not found."}, status=status.HTTP_404_NOT_FOUND
                )

            # Ensure the doctor is assigned to this visit
            if visit.assigned_doctor != doctor:
                return Response(
                    {"detail": "Doctor is not assigned to this visit."},
                    status=status.HTTP_403_FORBIDDEN,
                )

            # Fetch previous medical histories of the patient
            previous_histories = MedicalHistory.objects.filter(patient=visit.patient)

            # Create a new medical history entry for the current consultation
            MedicalHistory.objects.create(
                visit=visit,
                patient=visit.patient,
                description=new_history,
                recorded_by=doctor,
            )

            # Return the previous histories and a success message
            return Response(
                {
                    "detail": "Consultation completed.",
                    "previous_histories": [
                        {"id": h.id, "description": h.description, "date": h.created_at}
                        for h in previous_histories
                    ],
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            # Log the error for debugging purposes and send a generic error message
            return Response(
                {"detail": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# --- Medical History ---
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


class CompletePaymentView(APIView):
    def post(self, request):
        """
        Mark a payment as completed.
        """
        try:
            payment_id = request.data.get("payment_id")

            if not payment_id:
                return Response(
                    {"detail": "Payment ID is required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Fetch the payment
            try:
                payment = Payment.objects.get(id=payment_id)
            except Payment.DoesNotExist:
                return Response(
                    {"detail": "Payment not found."}, status=status.HTTP_404_NOT_FOUND
                )

            # Check if the payment is already completed
            if payment.status == "completed":
                return Response(
                    {"detail": "Payment is already marked as completed."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Update payment status
            payment.status = "completed"
            payment.save()

            return Response(
                {"detail": "Payment completed successfully."}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"detail": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


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
