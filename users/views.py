from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from django.contrib.auth.hashers import make_password
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
        data = request.data
        print(data)  # Debugging step

        try:
            # Get the department instance if provided
            department_id = data.get("department")
            department = Department.objects.get(id=department_id) if department_id else None

            user = User.objects.create(
                first_name=data.get("first_name", ""),
                middle_name=data.get("middle_name", ""),
                last_name=data.get("last_name", ""),
                email=data["email"],
                phone=data.get("phone", ""),
                qualification=data.get("qualification", ""),
                gender=data.get("gender", None),
                date_of_birth=data.get("date_of_birth", None),
                department=department,
                role=data["role"],
                is_staff=data.get("is_staff", False),
                is_active=data.get("is_active", True),
                password=make_password(data["password"]),  # Hash password
            )

            serializer = UserSerializer(user, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Department.DoesNotExist:
            return Response({"detail": "Invalid department ID"}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            message = {"detail": "User with this email or phone already exists"}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)






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
        data = request.data

        try:
            # Retrieve department if provided
            department_id = data.get("department")
            department = Department.objects.get(id=department_id) if department_id else None

            # Update user fields
            user.first_name = data.get("first_name", user.first_name)
            user.middle_name = data.get("middle_name", user.middle_name)
            user.last_name = data.get("last_name", user.last_name)
            user.email = data.get("email", user.email)
            user.phone = data.get("phone", user.phone)
            user.qualification = data.get("qualification", user.qualification)
            user.gender = data.get("gender", user.gender)
            user.date_of_birth = data.get("date_of_birth", user.date_of_birth)
            user.department = department
            user.role = data.get("role", user.role)
            user.is_staff = data.get("is_staff", user.is_staff)
            user.is_active = data.get("is_active", user.is_active)

            # Handle password update
            if data.get("password"):
                user.password = make_password(data["password"])

            user.save()

            serializer = UserSerializer(user, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Department.DoesNotExist:
            return Response({"detail": "Invalid department ID"}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        """
        Partially update a user record.
        """
        return self.put(request, pk)  # Since put already handles partial updates safely

    def delete(self, request, pk):
        """
        Delete a user.
        """
        user = self.get_object(pk)
        user.delete()
        return Response({"detail": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)



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
