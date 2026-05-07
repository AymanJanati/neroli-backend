from rest_framework import serializers

from leads.models import Lead
from properties.models import Property
from .models import Opportunity, PipelineStage


# ---------------------------------------------------------------------------
# Pipeline stage
# ---------------------------------------------------------------------------

class PipelineStageSerializer(serializers.ModelSerializer):
    """
    GET /api/admin/pipeline-stages/
    Response: { id, name, slug, order }
    """

    class Meta:
        model = PipelineStage
        fields = ["id", "name", "slug", "order"]


# ---------------------------------------------------------------------------
# Nested helpers
# ---------------------------------------------------------------------------

class BriefLeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = ["id", "full_name", "phone", "email"]


class BriefPropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ["id", "title_fr", "title_ar", "price", "status"]


class BriefStageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PipelineStage
        fields = ["id", "name", "slug"]


# ---------------------------------------------------------------------------
# Opportunity serializers
# ---------------------------------------------------------------------------

class OpportunityListSerializer(serializers.ModelSerializer):
    """
    Paginated list — GET /api/admin/opportunities/
    Nested brief lead, property, stage per contract §10.1
    """

    lead     = BriefLeadSerializer(read_only=True)
    property = BriefPropertySerializer(read_only=True)
    stage    = BriefStageSerializer(read_only=True)

    class Meta:
        model = Opportunity
        fields = [
            "id",
            "lead",
            "property",
            "stage",
            "status",
            "notes",
            "created_at",
            "updated_at",
        ]


class OpportunityDetailSerializer(serializers.ModelSerializer):
    """
    Full detail — GET /api/admin/opportunities/{id}/
    Includes lead (full brief), property (brief), stage (brief), interactions list.
    """

    lead        = BriefLeadSerializer(read_only=True)
    property    = BriefPropertySerializer(read_only=True)
    stage       = BriefStageSerializer(read_only=True)
    interactions = serializers.SerializerMethodField()

    class Meta:
        model = Opportunity
        fields = [
            "id",
            "lead",
            "property",
            "stage",
            "status",
            "notes",
            "interactions",
            "created_at",
            "updated_at",
        ]

    def get_interactions(self, obj):
        """Return all interactions linked to this opportunity, ordered by date."""
        from interactions.serializers import InteractionSerializer
        qs = obj.interactions.order_by("-interaction_date")
        return InteractionSerializer(qs, many=True).data


class OpportunityCreateUpdateSerializer(serializers.ModelSerializer):
    """
    POST / PATCH — accepts lead_id, property_id, stage_id.
    Returns OpportunityDetailSerializer shape on save.
    """

    lead_id     = serializers.PrimaryKeyRelatedField(
        queryset=Lead.objects.all(), source="lead"
    )
    property_id = serializers.PrimaryKeyRelatedField(
        queryset=Property.objects.all(), source="property"
    )
    stage_id    = serializers.PrimaryKeyRelatedField(
        queryset=PipelineStage.objects.all(), source="stage", required=False, allow_null=True
    )

    class Meta:
        model = Opportunity
        fields = ["lead_id", "property_id", "stage_id", "notes"]


class MoveStageSerializer(serializers.Serializer):
    """Input serializer for PATCH /api/admin/opportunities/{id}/move-stage/"""

    stage_id = serializers.PrimaryKeyRelatedField(queryset=PipelineStage.objects.all())
