from rest_framework import serializers
from users.models import Department, CustomUser as User
from .models import (
    Patient,
    Visit,
    Payment,
    PaymentItem,
    Vitals,
    MedicalHistory,
    Test,
    Prescription,
    Invoice,
    InvoiceItem,
    InsuranceCompany,
    HospitalItem,
    Insurance,  # Don't forget to import your Insurance model
)


class InsuranceCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceCompany
        fields = "__all__"


class HospitalItemSerializer(serializers.ModelSerializer):
    insurance_companies = InsuranceCompanySerializer(many=True, read_only=True)

    class Meta:
        model = HospitalItem
        fields = "__all__"


class InsuranceSerializer(serializers.ModelSerializer):
    provider = InsuranceCompanySerializer(
        read_only=True
    )  # Showing insurance provider details
    patient = serializers.PrimaryKeyRelatedField(
        queryset=Patient.objects.all(), write_only=True
    )  # Accept patient ID

    class Meta:
        model = Insurance
        fields = "__all__"


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = "__all__"


class VisitSerializer(serializers.ModelSerializer):
    department_name = serializers.SerializerMethodField()
    doctor_name = serializers.SerializerMethodField()
    patient_details = PatientSerializer(
        source="patient", read_only=True
    )  # Full patient details in GET responses

    department = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(), write_only=True  # Accept ID in input
    )
    assigned_doctor = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role="doctor"),  # Ensure only doctors are listed
        write_only=True,  # Accept ID in input
    )
    patient = serializers.PrimaryKeyRelatedField(
        queryset=Patient.objects.all(),
        write_only=True,  # Accept only patient ID in input
    )

    class Meta:
        model = Visit
        fields = "__all__"
        extra_kwargs = {
            "patient": {"write_only": True},  # Ensure patient ID is accepted in input
        }

    def get_department_name(self, obj):
        return obj.department.name if obj.department else None

    def get_doctor_name(self, obj):
        if obj.assigned_doctor:
            return f"{obj.assigned_doctor.first_name} {obj.assigned_doctor.last_name}"
        return None


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class PaymentItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentItem
        fields = "__all__"


class VitalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vitals
        fields = "__all__"


class MedicalHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalHistory
        fields = "__all__"


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = "__all__"


class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = "__all__"


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = "__all__"


class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = "__all__"
