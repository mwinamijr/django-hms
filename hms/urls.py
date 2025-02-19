import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


def custom_404_handler(request, exception):
    return JsonResponse(
        {
            "error": "Page Not Found",
            "detail": f"The requested URL {request.path} was not found on this server.",
        },
        status=404,
    )


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/users/", include("api.users.urls")),
    path("api/core/", include("api.core.urls")),
    path("api/management/", include("api.management.urls")),
    path("api/payments/", include("api.payments.urls")),
    path("__debug__/", include(debug_toolbar.urls)),
]


handler404 = custom_404_handler
