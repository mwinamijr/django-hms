from rest_framework import serializers
from .models import CustomUser, Department
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "role",
            "department",
            "last_name",
            "is_staff",
            "is_active",
            "date_joined",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        """
        Overriding the create method to handle password hashing.
        """
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        """
        Overriding the update method to handle password hashing.
        """
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["id", "name", "description", "created_at", "updated_at"]
