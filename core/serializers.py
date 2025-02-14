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
    Insurance,
    ItemType
)


class InsuranceCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceCompany
        fields = "__all__"


class ItemTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemType
        fields = "__all__"


class HospitalItemSerializer(serializers.ModelSerializer):
    insurance_companies = InsuranceCompanySerializer(many=True, read_only=True)
    insurance_company_ids = serializers.PrimaryKeyRelatedField(
        queryset=InsuranceCompany.objects.all(),
        many=True,
        write_only=True,
        required=False
    )

    item_type = ItemTypeSerializer(read_only=True)
    item_type_id = serializers.PrimaryKeyRelatedField(
        queryset=ItemType.objects.all(),
        write_only=True,
        required=False
    )

    class Meta:
        model = HospitalItem
        fields = ["id", "name", "price", "description", "is_active", "item_type", "item_type_id", "insurance_companies", "insurance_company_ids", "created_at", "updated_at"]

    def update(self, instance, validated_data):
        insurance_company_ids = validated_data.pop("insurance_company_ids", None)
        item_type_id = validated_data.pop("item_type_id", None)

        if insurance_company_ids is not None:
            instance.insurance_companies.set(insurance_company_ids)

        if item_type_id is not None:
            instance.item_type = item_type_id

        instance.save()
        return super().update(instance, validated_data)

    def create(self, validated_data):
        insurance_company_ids = validated_data.pop("insurance_company_ids", [])
        item_type_id = validated_data.pop("item_type_id", None)
        hospital_item = HospitalItem.objects.create(**validated_data)

        if insurance_company_ids:
            hospital_item.insurance_companies.set(insurance_company_ids)

        if item_type_id:
            hospital_item.item_type = item_type_id
            hospital_item.save()

        return hospital_item


class ItemTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemType
        fields = "__all__"


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = "__all__"


class InsuranceSerializer(serializers.ModelSerializer):
    provider = InsuranceCompanySerializer(read_only=True)
    provider_id = serializers.PrimaryKeyRelatedField(
        queryset=InsuranceCompany.objects.all(), write_only=True, source="provider"
    )  # Accept provider_id but assign it to the provider relationship

    patient = serializers.PrimaryKeyRelatedField(
        queryset=Patient.objects.all(), write_only=True
    )  # Accept patient ID
    insured_patient = PatientSerializer(source="patient", read_only=True)

    class Meta:
        model = Insurance
        fields = ["id", "policy_number", "patient", "provider", "provider_id", "insured_patient"]



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
