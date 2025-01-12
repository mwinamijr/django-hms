from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet, DepartmentViewSet

router = DefaultRouter()
router.register(r"", UserViewSet)
router.register(r"departments", DepartmentViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
