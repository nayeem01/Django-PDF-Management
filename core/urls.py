from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("documents.urls")),
    path("api/", include("utils.urls")),
    path("auth/", include("accounts.urls")),
]
