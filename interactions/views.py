from rest_framework import mixins, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import InteractionFilter
from .models import Interaction
from .serializers import InteractionSerializer


class InteractionViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    Interactions log — authentication required.
    No retrieve (single-object GET) per contract scope.

    GET    /api/admin/interactions/         → list (paginated, filterable)
    POST   /api/admin/interactions/         → create
    PATCH  /api/admin/interactions/{id}/    → partial update
    DELETE /api/admin/interactions/{id}/    → delete
    """

    permission_classes = [IsAuthenticated]
    serializer_class   = InteractionSerializer
    filterset_class    = InteractionFilter
    ordering_fields    = ["interaction_date", "created_at"]
    ordering           = ["-interaction_date"]

    def get_queryset(self):
        return Interaction.objects.select_related(
            "lead", "property", "opportunity"
        ).all()

    def update(self, request, *args, **kwargs):
        kwargs["partial"] = True  # PATCH only
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            {"detail": "Interaction deleted successfully."},
            status=status.HTTP_200_OK,
        )
