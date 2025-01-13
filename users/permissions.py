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


class IsCashier(BasePermission):
    """
    Custom permission to only allow users with the cashier role to access the view.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated and has the 'cashier' role
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == "cashier"
        )
