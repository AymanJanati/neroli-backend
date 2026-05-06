"""
Public property URLs — no auth required.
Mounted at: /api/public/
"""
from django.urls import path
from properties.views import PublicPropertyListView, PublicPropertyDetailView

urlpatterns = [
    path("properties/", PublicPropertyListView.as_view(), name="public-property-list"),
    path("properties/<int:pk>/", PublicPropertyDetailView.as_view(), name="public-property-detail"),
]
