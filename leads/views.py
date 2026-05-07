from rest_framework import mixins, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import LeadFilter
from .models import Lead, LeadPropertyInterest
from .serializers import (
    LeadCreateUpdateSerializer,
    LeadDetailSerializer,
    LeadListSerializer,
    LeadPropertyInterestSerializer,
)


class LeadViewSet(viewsets.ModelViewSet):
    """
    Admin CRUD for leads — authentication required.

    GET    /api/admin/leads/         → list   (paginated, filterable)
    POST   /api/admin/leads/         → create
    GET    /api/admin/leads/{id}/    → detail (with related properties, opportunities, interactions)
    PATCH  /api/admin/leads/{id}/    → partial update
    DELETE /api/admin/leads/{id}/    → delete
    """

    permission_classes = [IsAuthenticated]
    filterset_class    = LeadFilter
    search_fields      = ["full_name", "phone", "email"]
    ordering_fields    = ["created_at", "full_name"]
    ordering           = ["-created_at"]

    def get_queryset(self):
        return Lead.objects.all().prefetch_related(
            "property_interests__property",
            "opportunities__stage",
            "opportunities__property",
            "interactions",
        )

    def get_serializer_class(self):
        if self.action == "list":
            return LeadListSerializer
        if self.action in ("create", "update", "partial_update"):
            return LeadCreateUpdateSerializer
        return LeadDetailSerializer

    def create(self, request, *args, **kwargs):
        serializer = LeadCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        lead = serializer.save()
        return Response(
            LeadDetailSerializer(lead).data,
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        kwargs["partial"] = True  # PATCH only
        instance = self.get_object()
        serializer = LeadCreateUpdateSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        lead = serializer.save()
        return Response(LeadDetailSerializer(lead).data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"detail": "Lead deleted successfully."}, status=status.HTTP_200_OK)


class LeadPropertyInterestViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    Create and delete lead–property interest links.

    POST   /api/admin/lead-property-interests/       → create interest
    DELETE /api/admin/lead-property-interests/{id}/  → remove interest
    """

    permission_classes = [IsAuthenticated]
    serializer_class   = LeadPropertyInterestSerializer
    queryset           = LeadPropertyInterest.objects.select_related("lead", "property").all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"detail": "Interest deleted successfully."}, status=status.HTTP_200_OK)
