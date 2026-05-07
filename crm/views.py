from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from properties.models import Property

from .filters import OpportunityFilter
from .models import Opportunity, PipelineStage
from .serializers import (
    MoveStageSerializer,
    OpportunityCreateUpdateSerializer,
    OpportunityDetailSerializer,
    OpportunityListSerializer,
    PipelineStageSerializer,
)


class PipelineStageViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    GET /api/admin/pipeline-stages/

    Read-only list of all pipeline stages, ordered by `order`.
    Returns a plain list (not paginated) — 8 fixed stages.
    """

    permission_classes = [IsAuthenticated]
    serializer_class   = PipelineStageSerializer
    queryset           = PipelineStage.objects.all()
    pagination_class   = None  # return a flat array, not paginated


class OpportunityViewSet(viewsets.ModelViewSet):
    """
    Admin CRUD for opportunities + move-stage action.

    GET    /api/admin/opportunities/                    → list (paginated, filterable)
    POST   /api/admin/opportunities/                    → create
    GET    /api/admin/opportunities/{id}/               → detail
    PATCH  /api/admin/opportunities/{id}/               → partial update
    PATCH  /api/admin/opportunities/{id}/move-stage/    → move through pipeline
    DELETE /api/admin/opportunities/{id}/               → delete
    """

    permission_classes = [IsAuthenticated]
    filterset_class    = OpportunityFilter
    ordering_fields    = ["created_at", "updated_at"]
    ordering           = ["-created_at"]

    def get_queryset(self):
        return Opportunity.objects.select_related(
            "lead", "property", "stage"
        ).prefetch_related("interactions").all()

    def get_serializer_class(self):
        if self.action == "list":
            return OpportunityListSerializer
        if self.action in ("create", "update", "partial_update"):
            return OpportunityCreateUpdateSerializer
        return OpportunityDetailSerializer

    def create(self, request, *args, **kwargs):
        serializer = OpportunityCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        opp = serializer.save()
        return Response(
            OpportunityDetailSerializer(opp).data,
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        kwargs["partial"] = True  # PATCH only
        instance = self.get_object()
        serializer = OpportunityCreateUpdateSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        opp = serializer.save()
        return Response(OpportunityDetailSerializer(opp).data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            {"detail": "Opportunity deleted successfully."},
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["patch"], url_path="move-stage")
    def move_stage(self, request, pk=None):
        """
        PATCH /api/admin/opportunities/{id}/move-stage/
        Request:  { "stage_id": <int> }

        Business rules (Backend–Backend Contract §6.6):
          - stage.slug == "sold"     → opportunity.status = "won",  property.status = "sold"
          - stage.slug == "lost"     → opportunity.status = "lost"
          - stage.slug == "reserved" → property.status = "reserved"
          - any other stage          → no automatic status changes

        Moving BACK (from sold/reserved to earlier stage):
          - opportunity.status is reset to "open" if it was auto-set
          - property.status is NOT auto-reverted (another opportunity may have set it).
            This is documented MVP behaviour.
        """
        opportunity = self.get_object()

        input_serializer = MoveStageSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        new_stage = input_serializer.validated_data["stage_id"]

        old_stage_slug = opportunity.stage.slug if opportunity.stage else None

        # Apply business rules
        new_slug = new_stage.slug

        if new_slug == "sold":
            opportunity.status = Opportunity.Status.WON
            opportunity.property.status = Property.Status.SOLD
            opportunity.property.save(update_fields=["status"])
        elif new_slug == "lost":
            opportunity.status = Opportunity.Status.LOST
        elif new_slug == "reserved":
            opportunity.property.status = Property.Status.RESERVED
            opportunity.property.save(update_fields=["status"])
        else:
            # Moving to any non-terminal stage — reset status to open
            # if it was previously auto-set by a sold/lost transition
            if opportunity.status in (Opportunity.Status.WON, Opportunity.Status.LOST):
                opportunity.status = Opportunity.Status.OPEN

        opportunity.stage = new_stage
        opportunity.save(update_fields=["stage", "status", "updated_at"])

        return Response(
            {
                "id": opportunity.id,
                "stage": PipelineStageSerializer(new_stage).data,
                "status": opportunity.status,
                "updated_at": opportunity.updated_at,
            }
        )
