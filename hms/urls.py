import debug_toolbar
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/users/", include("api.users.urls")),
    path("api/core/", include("api.core.urls")),
    path("api/payments/", include("api.payments.urls")),
    path("__debug__/", include(debug_toolbar.urls)),
]
