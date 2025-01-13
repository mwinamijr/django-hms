from django.urls import path
from rest_framework_simplejwt import views
from users.views import (
    UserListView,
    UserDetailView,
    DepartmentListView,
    DepartmentDetailView,
    LoginView,
)

urlpatterns = [
    path("", LoginView.as_view(), name="token_refresh"),
    path("refresh/token/", views.TokenRefreshView.as_view(), name="token-refresh"),
    # Users
    path("users/", UserListView.as_view(), name="user_list"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user_detail"),
    # Departments
    path("departments/", DepartmentListView.as_view(), name="department_list"),
    path(
        "departments/<int:pk>/",
        DepartmentDetailView.as_view(),
        name="department_detail",
    ),
]
