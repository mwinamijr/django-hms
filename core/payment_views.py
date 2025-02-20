import logging
from decimal import Decimal
from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.permissions import IsCashier
from .models import (
    Visit,
    Insurance,
    Test,
    Prescription,
    Invoice,
    InvoiceItem,
    Payment,
    PaymentItem,
    HospitalItem,
)
from .serializers import (
    InvoiceSerializer,
    InvoiceItemSerializer,
    PaymentSerializer,
    PaymentItemSerializer,
)


# Set up logging
logger = logging.getLogger(__name__)


class ConsultationPaymentView(APIView):
    def post(self, request):
        """
        Handle consultation payments for both cash and insured patients.
        """
        print(request.data)
        try:
            # Extract visit ID from request
            visit_id = request.data.get("visit_id")

            if not visit_id:
                return Response(
                    {"detail": "Visit ID is required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Fetch the visit
            try:
                visit = Visit.objects.get(id=visit_id)
            except Visit.DoesNotExist:
                return Response(
                    {"detail": "Visit not found."}, status=status.HTTP_404_NOT_FOUND
                )

            # Check if the patient is insured
            is_insured = Insurance.objects.filter(patient=visit.patient).exists()

            # Fetch the "Consultation Fee" HospitalItem
            try:
                consultation_item = HospitalItem.objects.get(
                    name__iexact="Consultation Fee"
                )
                consultation_fee = consultation_item.price
            except HospitalItem.DoesNotExist:
                return Response(
                    {"detail": "Consultation Fee item not found."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if is_insured:
                # Check if an insurance invoice already exists for this visit
                invoice, created = Invoice.objects.get_or_create(
                    visit=visit,
                    defaults={"total_amount": 0, "is_insurance": True},
                )

                if invoice:
                    # Prevent duplicate consultation charge
                    if InvoiceItem.objects.filter(
                        invoice=invoice, item=consultation_item
                    ).exists():
                        return Response(
                            {
                                "detail": "Consultation invoice already exists for this visit.",
                                "invoice_id": invoice.id,
                                "total_amount": str(invoice.total_amount),
                            },
                            status=status.HTTP_400_BAD_REQUEST,
                        )

                    # Add consultation fee to invoice
                    InvoiceItem.objects.create(invoice=invoice, item=consultation_item)
                    invoice.total_amount = consultation_fee
                    invoice.save()

                return Response(
                    {
                        "detail": "Consultation invoice generated successfully for insurance.",
                        "invoice_id": invoice.id,
                        "total_amount": str(invoice.total_amount),
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                # Check if an payment for this visit already exists
                payment, created = Payment.objects.get_or_create(
                    visit=visit,
                    defaults={"amount": 0, "status": "pending"},
                )
                print("payment", payment)
                print(
                    "if exist:",
                    PaymentItem.objects.filter(
                        payment=payment, item=consultation_item
                    ).exists(),
                )

                print("not created", not created)
                if payment:
                    # Prevent duplicate consultation charge
                    if PaymentItem.objects.filter(
                        payment=payment, item=consultation_item
                    ).exists():
                        return Response(
                            {
                                "detail": "Consultation payment already exists for this visit.",
                                "payment_id": payment.id,
                                "amount": str(payment.amount),
                            },
                            status=status.HTTP_400_BAD_REQUEST,
                        )

                    # Add consultation fee to payment
                    PaymentItem.objects.create(payment=payment, item=consultation_item)
                    print(
                        "created",
                        PaymentItem.objects.filter(
                            payment=payment, item=consultation_item
                        ),
                    )

                    payment.amount = consultation_fee
                    payment.save()

                return Response(
                    {
                        "detail": "Cash payment for consultation fee processed successfully.",
                        "payment_id": payment.id,
                        "amount": str(consultation_fee),
                        "status": payment.status,
                    },
                    status=status.HTTP_200_OK,
                )

        except Exception as e:
            return Response(
                {"detail": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class GenerateTestPaymentView(APIView):
    def post(self, request):
        """
        Generate a payment for assigned tests, handling both cash and insurance patients.
        """
        try:
            # Extract data from the request
            visit_id = request.data.get("visit_id")
            # is_insured = request.data.get("is_insured", False)
            insurance_coverage = Decimal(request.data.get("insurance_coverage", "0.00"))

            if not visit_id:
                return Response(
                    {"detail": "Visit ID is required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Fetch the visit
            try:
                visit = Visit.objects.get(id=visit_id)
            except Visit.DoesNotExist:
                return Response(
                    {"detail": "Visit not found."}, status=status.HTTP_404_NOT_FOUND
                )

            # Fetch pending tests associated with the visit
            tests = Test.objects.filter(visit=visit, status="pending")
            if not tests.exists():
                return Response(
                    {"detail": "No pending tests to generate payment for."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Calculate the total price for pending tests
            total_price = sum(test.price for test in tests)

            # Check if the patient is insured
            is_insured = visit.patient.payment_method == "insurance"

            if is_insured:
                # Handle insured patient
                remaining_cost = total_price - insurance_coverage
                covered_tests = []
                uncovered_tests = []

                # Classify tests based on insurance coverage
                for test in tests:
                    if insurance_coverage >= test.price:
                        covered_tests.append(test)
                        insurance_coverage -= test.price
                    else:
                        uncovered_tests.append(test)

                # Generate invoice for covered tests
                if covered_tests:
                    invoice, _ = Invoice.objects.get_or_create(
                        visit=visit,
                        defaults={"total_amount": 0, "is_insurance": True},
                    )
                    for test in covered_tests:
                        InvoiceItem.objects.create(
                            invoice=invoice,
                            description=test.name,
                            category="test",
                            amount=test.price,
                        )
                        test.status = "insurance"  # Mark test as covered by insurance
                        test.save()

                    invoice.total_amount += sum(test.price for test in covered_tests)
                    invoice.save()

                # Generate payment for uncovered tests
                if uncovered_tests:
                    payment = Payment.objects.create(
                        visit=visit,
                        amount=remaining_cost,
                        status="pending",
                    )
                    for test in uncovered_tests:
                        PaymentItem.objects.create(
                            payment=payment,
                            description=test.name,
                            type="test",
                            price=test.price,
                        )
                    return Response(
                        {
                            "detail": "Payment generated successfully for uncovered tests.",
                            "payment_id": payment.id,
                            "uncovered_amount": remaining_cost,
                            "total_insurance_covered": total_price - remaining_cost,
                        },
                        status=status.HTTP_200_OK,
                    )

                return Response(
                    {
                        "detail": "Invoice generated successfully for covered tests.",
                        "total_insurance_covered": total_price,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                # Handle cash payment
                payment = Payment.objects.create(
                    visit=visit,
                    amount=total_price,
                    status="pending",
                )
                for test in tests:
                    PaymentItem.objects.create(
                        payment=payment,
                        description=test.name,
                        type="test",
                        price=test.price,
                    )
                    test.status = "pending_payment"
                    test.save()

                return Response(
                    {
                        "detail": "Payment generated successfully for tests.",
                        "total_amount": total_price,
                        "payment_id": payment.id,
                    },
                    status=status.HTTP_200_OK,
                )

        except Exception as e:
            return Response(
                {"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GeneratePrescriptionPaymentView(APIView):
    def post(self, request):
        """
        Generate a payment for prescribed medicines, handling both cash and insurance patients.
        """
        try:
            # Extract data from the request
            visit_id = request.data.get("visit_id")
            # is_insured = request.data.get("is_insured", False)
            insurance_coverage = Decimal(request.data.get("insurance_coverage", "0.00"))

            if not visit_id:
                return Response(
                    {"detail": "Visit ID is required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Fetch the visit
            try:
                visit = Visit.objects.get(id=visit_id)
            except Visit.DoesNotExist:
                return Response(
                    {"detail": "Visit not found."}, status=status.HTTP_404_NOT_FOUND
                )

            # Fetch prescriptions for the visit
            prescriptions = Prescription.objects.filter(visit=visit)
            if not prescriptions.exists():
                return Response(
                    {"detail": "No prescriptions to generate payment."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Calculate the total price for all prescriptions
            total_price = sum(prescription.price for prescription in prescriptions)

            # Check if the patient has insurance
            is_insured = visit.patient.payment_method == "insurance"

            if is_insured:
                # Handle insured patient
                remaining_cost = total_price - insurance_coverage
                covered_medicines = []
                uncovered_medicines = []

                # Classify prescriptions based on insurance coverage
                for prescription in prescriptions:
                    if insurance_coverage >= prescription.price:
                        covered_medicines.append(prescription)
                        insurance_coverage -= prescription.price
                    else:
                        uncovered_medicines.append(prescription)

                # Generate invoice for covered medicines
                if covered_medicines:
                    invoice, _ = Invoice.objects.get_or_create(
                        visit=visit,
                        defaults={"total_amount": 0, "is_insurance": True},
                    )
                    for prescription in covered_medicines:
                        InvoiceItem.objects.create(
                            invoice=invoice,
                            description=f"Medicine: {prescription.medicine_name}",
                            category="medicine",
                            amount=prescription.price,
                        )
                    invoice.total_amount += sum(
                        prescription.price for prescription in covered_medicines
                    )
                    invoice.save()

                # Generate payment for uncovered medicines
                if uncovered_medicines:
                    payment = Payment.objects.create(
                        visit=visit,
                        amount=remaining_cost,
                        status="pending",
                    )
                    for prescription in uncovered_medicines:
                        PaymentItem.objects.create(
                            payment=payment,
                            description=f"Medicine: {prescription.medicine_name}",
                            type="prescription",
                            price=prescription.price,
                        )
                    return Response(
                        {
                            "detail": "Payment generated successfully for uncovered medicines.",
                            "payment_id": payment.id,
                            "uncovered_amount": remaining_cost,
                            "total_insurance_covered": total_price - remaining_cost,
                        },
                        status=status.HTTP_200_OK,
                    )

                return Response(
                    {
                        "detail": "Invoice generated successfully for covered medicines.",
                        "total_insurance_covered": total_price,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                # Handle cash payment
                payment = Payment.objects.create(
                    visit=visit,
                    amount=total_price,
                    status="pending",
                )
                for prescription in prescriptions:
                    PaymentItem.objects.create(
                        payment=payment,
                        description=f"Medicine: {prescription.medicine_name}",
                        type="prescription",
                        price=prescription.price,
                    )

                return Response(
                    {
                        "detail": "Payment generated successfully for prescribed medicines.",
                        "total_amount": total_price,
                        "payment_id": payment.id,
                    },
                    status=status.HTTP_200_OK,
                )

        except Exception as e:
            return Response(
                {"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CompletePaymentView(APIView):
    """
    Mark a payment as completed. Only accessible to users with the cashier role.
    """

    permission_classes = [IsCashier]

    def post(self, request, visit_id):
        print(request.data)
        try:
            # Step 1: Validate input
            payment_id = request.data.get("payment_id")
            item_ids = request.data.get(
                "item_ids", []
            )  # Expecting a list of payment item IDs
            print("paymentId:", payment_id)
            print("item ids:", item_ids)

            if not payment_id:
                return Response(
                    {"detail": "Payment ID is required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Step 2: Retrieve the payment record
            try:
                payment = Payment.objects.get(id=payment_id)
            except Payment.DoesNotExist:
                return Response(
                    {"detail": f"Payment with ID {payment_id} not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Step 3: Check payment status
            if payment.status == "completed":
                return Response(
                    {"detail": f"Payment with ID {payment_id} is already completed."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Step 4: Update provided paymentItems to "completed"
            with transaction.atomic():
                updated_count = PaymentItem.objects.filter(
                    id__in=item_ids, payment=payment
                ).update(status="completed")

                # Step 5: Check if all paymentItems for this payment are completed
                all_completed = not PaymentItem.objects.filter(
                    payment=payment, status="pending"
                ).exists()

                if all_completed:
                    payment.status = "completed"
                    payment.save()

            return Response(
                {
                    "detail": f"{updated_count} Payment Item(s) updated successfully.",
                    "payment_status": "completed" if all_completed else "pending",
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"detail": f"Error completing payment {payment_id}: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# --- Invoice For Insured Patients Management ---


class SubmitToInsuranceView(APIView):
    def post(self, request):
        """
        Submit all insurance invoices for a visit to the insurance provider.
        """
        try:
            # Extract visit ID from the request body
            visit_id = request.data.get("visit_id")

            if not visit_id:
                return Response(
                    {"detail": "Visit ID is required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Fetch the visit associated with the visit ID
            try:
                visit = Visit.objects.get(id=visit_id)
            except Visit.DoesNotExist:
                return Response(
                    {"detail": "Visit not found."}, status=status.HTTP_404_NOT_FOUND
                )

            # Fetch all unpaid insurance-related invoices for the visit
            invoices = Invoice.objects.filter(
                visit=visit, is_insurance=True, is_paid=False
            )

            if not invoices.exists():
                return Response(
                    {"detail": "No pending insurance invoices found."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Simulate submission to the insurance provider
            for invoice in invoices:
                # Simulate an API call or submission process
                logger.info(
                    f"Submitting Invoice {invoice.id} for Visit {visit.id} to insurance provider."
                )

                # Mark invoice as paid after submission (simulate successful submission)
                invoice.is_paid = True
                invoice.save()

                # Log the action
                logger.info(
                    f"Invoice {invoice.id} for Visit {visit.id} marked as paid."
                )

            # Return success response
            return Response(
                {
                    "detail": "All pending insurance invoices submitted successfully.",
                    "visit_id": visit_id,
                    "submitted_invoices": invoices.count(),
                },
                status=status.HTTP_200_OK,
            )

        except Visit.DoesNotExist:
            return Response(
                {"detail": "Visit not found."}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            # Handle unexpected errors
            logger.error(f"Error submitting insurance invoices: {str(e)}")
            return Response(
                {"detail": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# Payment Views


class VisitPaymentItemListView(generics.ListAPIView):
    """
    API to list all payment items for a specific visit.
    """

    serializer_class = PaymentItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        visit_id = self.kwargs.get("visit_id")
        return PaymentItem.objects.filter(payment__visit_id=visit_id)


class VisitPaymentDetailView(generics.RetrieveAPIView):
    """
    API to retrieve a specific payment associated with a visit.
    """

    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        visit_id = self.kwargs.get("visit_id")
        return get_object_or_404(Payment, visit_id=visit_id)


class PaymentListView(APIView):
    # permission_classes = [IsCashier]

    def get(self, request):
        invoices = Payment.objects.all()
        serializer = PaymentSerializer(invoices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PaymentDetailView(APIView):
    # permission_classes = [IsCashier]

    def get_object(self, pk):
        return get_object_or_404(Payment, pk=pk)

    def get(self, request, pk):
        invoice = self.get_object(pk)
        serializer = PaymentSerializer(invoice)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PaymentItemListView(APIView):
    # permission_classes = [IsCashier]

    def get(self, request):
        invoices = PaymentItem.objects.all()
        serializer = PaymentItemSerializer(invoices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PaymentItemDetailView(APIView):
    # permission_classes = [IsCashier]

    def get_object(self, pk):
        return get_object_or_404(PaymentItem, pk=pk)

    def get(self, request, pk):
        invoice = self.get_object(pk)
        serializer = PaymentItemSerializer(invoice)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Invoice Views
class InvoiceListView(APIView):
    # permission_classes = [IsCashier]

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
    # permission_classes = [IsCashier]

    def get_object(self, pk):
        return get_object_or_404(Invoice, pk=pk)

    def get(self, request, pk):
        invoice = self.get_object(pk)
        serializer = InvoiceSerializer(invoice)
        return Response(serializer.data, status=status.HTTP_200_OK)


class InvoiceItemListView(APIView):
    # permission_classes = [IsCashier]

    def get(self, request):
        invoices = InvoiceItem.objects.all()
        serializer = InvoiceItemSerializer(invoices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = InvoiceItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InvoiceItemDetailView(APIView):
    # permission_classes = [IsCashier]

    def get_object(self, pk):
        return get_object_or_404(InvoiceItem, pk=pk)

    def get(self, request, pk):
        invoice = self.get_object(pk)
        serializer = InvoiceItemSerializer(invoice)
        return Response(serializer.data, status=status.HTTP_200_OK)
