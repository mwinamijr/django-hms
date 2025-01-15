from rest_framework.permissions import BasePermission


class IsDoctor(BasePermission):
    """
    Custom permission to only allow users with the doctor role to access the view.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated and has the 'doctor' role
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == "doctor"
        )


class IsNurse(BasePermission):
    """
    Custom permission to only allow users with the nurse role to access the view.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated and has the 'nurse' role
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == "nurse"
        )


class IsReceptionist(BasePermission):
    """
    Custom permission to only allow users with the receptionist role to access the view.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated and has the 'cashier' role
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == "receptionist"
        )


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
