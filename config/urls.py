"""
URL configuration for CyphX Real Estate Platform.

Public  → /api/public/
Auth    → /api/auth/
Admin   → /api/admin/
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("django-admin/", admin.site.urls),

    # Authentication
    path("api/auth/", include("accounts.urls")),

    # Public endpoints (no auth required)
    path("api/public/", include("core.urls.public")),
    path("api/public/", include("properties.urls.public")),

    # Admin/private endpoints (auth required)
    path("api/admin/", include("properties.urls.admin")),
    # PERSON_B — CRM & Sales
    path("api/admin/", include("leads.urls")),
    path("api/admin/", include("crm.urls")),
    path("api/admin/", include("interactions.urls")),
    path("api/admin/", include("dashboard.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
