from rest_framework.permissions import BasePermission


class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "doctor"


class IsNurse(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "nurse"


class IsReceptionist(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "receptionist"
