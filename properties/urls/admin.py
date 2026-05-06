"""
Admin property URLs — authentication required.
Mounted at: /api/admin/
"""
from django.urls import path
from rest_framework.routers import DefaultRouter
from properties.views import AdminPropertyViewSet, AdminPropertyImageDeleteView

router = DefaultRouter()
router.register(r"properties", AdminPropertyViewSet, basename="admin-property")

urlpatterns = router.urls + [
    path(
        "property-images/<int:pk>/",
        AdminPropertyImageDeleteView.as_view(),
        name="admin-property-image-delete",
    ),
]
