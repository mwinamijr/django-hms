from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from users.models import CustomUser as User
from .models import Insurance, HospitalItem, InsuranceCompany, ItemType, VisitComment
from .serializers import (
    InsuranceSerializer,
    HospitalItemSerializer,
    InsuranceCompanySerializer,
    ItemTypeSerializer,
    VisitCommentSerializer,
)
import openpyxl


class InsuranceListView(APIView):
    """
    Handles GET and POST requests for the list of insurances.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieve a list of all insurances.
        """
        insurances = Insurance.objects.all()
        serializer = InsuranceSerializer(insurances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create a new insurance record.
        """
        serializer = InsuranceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InsuranceDetailView(APIView):
    """
    Handles GET, PUT, PATCH, and DELETE requests for a single insurance.
    """

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Insurance, pk=pk)

    def get(self, request, pk):
        """
        Retrieve details of a specific insurance.
        """
        insurance = self.get_object(pk)
        serializer = InsuranceSerializer(insurance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """
        Update an entire insurance record.
        """
        insurance = self.get_object(pk)
        serializer = InsuranceSerializer(insurance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        """
        Partially update an insurance record.
        """
        insurance = self.get_object(pk)
        serializer = InsuranceSerializer(insurance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete an insurance record.
        """
        insurance = self.get_object(pk)
        insurance.delete()
        return Response(
            {"detail": "Insurance record deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class HospitalItemListView(APIView):
    """
    Handles GET and POST requests for the list of hospital items.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieve a list of all hospital items.
        """
        hospital_items = HospitalItem.objects.all()
        serializer = HospitalItemSerializer(hospital_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create a new hospital item record.
        """
        serializer = HospitalItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HospitalItemDetailView(APIView):
    """
    Handles GET, PUT, PATCH, and DELETE requests for a single hospital item.
    """

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(HospitalItem, pk=pk)

    def get(self, request, pk):
        """
        Retrieve details of a specific hospital item.
        """
        hospital_item = self.get_object(pk)
        serializer = HospitalItemSerializer(hospital_item)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """
        Update an entire hospital item record.
        """
        print(request.data)
        hospital_item = self.get_object(pk)
        serializer = HospitalItemSerializer(hospital_item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        """
        Partially update a hospital item record.
        """
        hospital_item = self.get_object(pk)
        serializer = HospitalItemSerializer(
            hospital_item, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete a hospital item record.
        """
        hospital_item = self.get_object(pk)
        hospital_item.delete()
        return Response(
            {"detail": "Hospital item deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class ItemTypeListView(APIView):
    """
    Handles GET and POST requests for the list of item types.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieve a list of all item types.
        """
        hospital_items = ItemType.objects.all()
        serializer = ItemTypeSerializer(hospital_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create a new item type record.
        """
        serializer = ItemTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ItemTypeDetailView(APIView):
    """
    Handles GET, PUT, PATCH, and DELETE requests for a single item type.
    """

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(ItemType, pk=pk)

    def get(self, request, pk):
        """
        Retrieve details of a specific item type.
        """
        hospital_item = self.get_object(pk)
        serializer = ItemTypeSerializer(hospital_item)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """
        Update an entire item type record.
        """
        print(request.data)
        hospital_item = self.get_object(pk)
        serializer = ItemTypeSerializer(hospital_item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        """
        Partially update a item type record.
        """
        hospital_item = self.get_object(pk)
        serializer = ItemTypeSerializer(hospital_item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete a item type record.
        """
        hospital_item = self.get_object(pk)
        hospital_item.delete()
        return Response(
            {"detail": "Item type deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class InsuranceCompanyListView(APIView):
    """
    Handles GET and POST requests for the list of insurance companies.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieve a list of all insurance companies.
        """
        insurance_companies = InsuranceCompany.objects.all()
        serializer = InsuranceCompanySerializer(insurance_companies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create a new insurance company record.
        """
        serializer = InsuranceCompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InsuranceCompanyDetailView(APIView):
    """
    Handles GET, PUT, PATCH, and DELETE requests for a single insurance company.
    """

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(InsuranceCompany, pk=pk)

    def get(self, request, pk):
        """
        Retrieve details of a specific insurance company.
        """
        insurance_company = self.get_object(pk)
        serializer = InsuranceCompanySerializer(insurance_company)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """
        Update an entire insurance company record.
        """
        print(request.data)
        insurance_company = self.get_object(pk)
        serializer = InsuranceCompanySerializer(insurance_company, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        """
        Partially update an insurance company record.
        """
        insurance_company = self.get_object(pk)
        serializer = InsuranceCompanySerializer(
            insurance_company, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete an insurance company record.
        """
        insurance_company = self.get_object(pk)
        insurance_company.delete()
        return Response(
            {"detail": "Insurance company deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class HospitalBulkUploadView(APIView):
    """
    API View to handle bulk uploading of hospital items from an Excel file.
    """

    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file = request.FILES.get("file")

        if not file:
            return Response(
                {"error": "No file provided."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            workbook = openpyxl.load_workbook(file)
            sheet = workbook.active

            required_columns = [
                "name",
                "description",
                "price",
                "item_type_id",
                "insurance_company_ids",
            ]

            excel_headers = [cell.value for cell in sheet[1]]

            if not all(col in excel_headers for col in required_columns):
                return Response(
                    {
                        "error": f"Missing columns. Expected: {', '.join(required_columns)}"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            created_items = []
            not_created = []

            for i, row in enumerate(
                sheet.iter_rows(min_row=2, values_only=True), start=2
            ):
                item_data = dict(zip(required_columns, row))

                try:
                    if not ItemType.objects.filter(
                        id=item_data["item_type_id"]
                    ).exists():
                        raise ValueError(
                            f"ItemType ID '{item_data['item_type_id']}' does not exist."
                        )

                    insurance_companies = []
                    if item_data["insurance_company_ids"]:
                        insurance_ids = str(item_data["insurance_company_ids"]).split(
                            ","
                        )
                        for insurance_id in insurance_ids:
                            insurance_obj = InsuranceCompany.objects.filter(
                                id=insurance_id.strip()
                            ).first()
                            if insurance_obj:
                                insurance_companies.append(insurance_obj)
                            else:
                                raise ValueError(
                                    f"InsuranceCompany ID '{insurance_id.strip()}' does not exist."
                                )

                    serializer = HospitalItemSerializer(data=item_data)

                    if serializer.is_valid():
                        hospital_item = serializer.save()

                        hospital_item.insurance_companies.set(insurance_companies)

                        created_items.append(serializer.data)
                    else:
                        raise ValueError(serializer.errors)

                except Exception as e:
                    item_data["error"] = str(e)
                    not_created.append(item_data)

            return Response(
                {
                    "message": f"{len(created_items)} hospital items successfully uploaded.",
                    "not_created": not_created,
                },
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class VisitCommentListView(APIView):
    """
    Handles listing all comments for a visit and creating new comments.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, visit_id):
        """Retrieve all comments for a given visit"""
        comments = VisitComment.objects.filter(visit__id=visit_id).order_by(
            "-created_at"
        )
        serializer = VisitCommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, visit_id):
        """Create a new visit comment and assign the logged-in user"""

        data = request.data.copy()
        data["visit"] = visit_id  # Ensure the visit ID is included

        serializer = VisitCommentSerializer(
            data=data, context={"request": request}
        )  # Pass request context
        if serializer.is_valid():
            serializer.save()  # Save the comment with `created_by`
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VisitCommentDeatilView(APIView):
    """
    Handles retrieving, updating, and deleting a single visit comment.
    """

    permission_classes = [IsAuthenticated]

    def get_object(self, comment_id):
        try:
            return VisitComment.objects.get(id=comment_id)
        except VisitComment.DoesNotExist:
            return None

    def get(self, request, comment_id):
        comment = self.get_object(comment_id)
        if not comment:
            return Response(
                {"detail": "Comment not found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = VisitCommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, comment_id):
        """Update a specific comment (only allowed for the creator)"""
        comment = self.get_object(comment_id)
        if not comment:
            return Response(
                {"detail": "Comment not found."}, status=status.HTTP_404_NOT_FOUND
            )

        if comment.created_by != request.user:
            raise PermissionDenied("You are not allowed to modify this comment.")

        serializer = VisitCommentSerializer(comment, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, comment_id):
        """Partially update a specific comment"""
        comment = self.get_object(comment_id)
        if not comment:
            return Response(
                {"detail": "Comment not found."}, status=status.HTTP_404_NOT_FOUND
            )

        if comment.created_by != request.user:
            raise PermissionDenied("You are not allowed to modify this comment.")

        serializer = VisitCommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, comment_id):
        """Delete a specific comment (only allowed for the creator)"""
        comment = self.get_object(comment_id)
        if not comment:
            return Response(
                {"detail": "Comment not found."}, status=status.HTTP_404_NOT_FOUND
            )

        if comment.created_by != request.user:
            raise PermissionDenied("You are not allowed to delete this comment.")

        comment.delete()
        return Response(
            {"detail": "Comment deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )
