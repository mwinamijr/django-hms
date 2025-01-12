from rest_framework import serializers
from .models import CustomUser, Department


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["id", "name"]


class UserSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)

    class Meta:
        model = CustomUser
        fields = ["id", "email", "first_name", "last_name", "role", "department"]
