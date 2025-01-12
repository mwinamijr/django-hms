from rest_framework import serializers
from .models import Patient, Visit, Payment, Vitals


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = "__all__"


class VisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class VitalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vitals
        fields = "__all__"
