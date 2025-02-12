from rest_framework import serializers
from .models import CustomUser as User, Department

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["id", "name", "short_name", "description", "created_at", "updated_at"]

class UserSerializer(serializers.ModelSerializer):
    department_name = serializers.SerializerMethodField()
    department = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(),
        write_only=True  # Allow input as an ID when creating/updating
    )

    class Meta:
        model = User
        fields = [
        "id",
        "last_login",
        "first_name",
        "middle_name",
        "last_name",
        "email",
        "phone",
        "qualification",
        "gender",
        "department",
        "department_name",
        "date_joined",
        "date_of_birth",
        "role",
        "is_staff",
        "is_active",
        ]
    
    def get_department_name(self, obj):
        return obj.department.name if obj.department else None

  