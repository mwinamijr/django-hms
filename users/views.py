from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import Department, CustomUser as User
from .serializers import UserSerializer, DepartmentSerializer


class LoginView(APIView):
    def post(self, request):
        """
        Authenticate user and return JWT tokens.
        """
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response(
                {"detail": "Email and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(email=email, password=password)

        if user is not None:
            # Generate tokens
            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "is_staff": user.is_staff,
                    },
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"detail": "Invalid email or password."},
                status=status.HTTP_401_UNAUTHORIZED,
            )


# User List View
class UserListView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        """
        List all users.
        """
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create a new user.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# User Detail View
class UserDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_object(self, pk):
        """
        Retrieve a specific user by primary key.
        """
        return get_object_or_404(User, pk=pk)

    def get(self, request, pk):
        """
        Retrieve user details.
        """
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """
        Fully update a user record.
        """
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        """
        Partially update a user record.
        """
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete a user.
        """
        user = self.get_object(pk)
        user.delete()
        return Response(
            {"detail": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )


# Department List View
class DepartmentListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        List all departments.
        """
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create a new department.
        """
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Department Detail View
class DepartmentDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        """
        Retrieve a specific department by primary key.
        """
        return get_object_or_404(Department, pk=pk)

    def get(self, request, pk):
        """
        Retrieve department details.
        """
        department = self.get_object(pk)
        serializer = DepartmentSerializer(department)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """
        Fully update a department record.
        """
        department = self.get_object(pk)
        serializer = DepartmentSerializer(department, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        """
        Partially update a department record.
        """
        department = self.get_object(pk)
        serializer = DepartmentSerializer(department, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete a department.
        """
        department = self.get_object(pk)
        department.delete()
        return Response(
            {"detail": "Department deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
