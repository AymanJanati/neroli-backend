from rest_framework import serializers

from properties.models import Property
from .models import Lead, LeadPropertyInterest


# ---------------------------------------------------------------------------
# Minimal nested serializers (used inside Lead detail)
# ---------------------------------------------------------------------------

class BriefPropertySerializer(serializers.ModelSerializer):
    """Minimal property representation embedded in lead detail."""

    class Meta:
        model = Property
        fields = ["id", "title_fr", "title_ar", "price", "status"]


class BriefOpportunitySerializer(serializers.Serializer):
    """
    Minimal opportunity snapshot embedded in lead detail.
    Defined here as a plain Serializer to avoid circular imports
    (crm app imports Lead; leads app would import Opportunity).
    Populated dynamically in LeadDetailSerializer.get_opportunities().
    """
    id       = serializers.IntegerField()
    stage    = serializers.CharField(source="stage.slug", default=None)
    status   = serializers.CharField()
    property = serializers.SerializerMethodField()

    def get_property(self, obj):
        if obj.property:
            return {
                "id": obj.property.id,
                "title_fr": obj.property.title_fr,
                "title_ar": obj.property.title_ar,
            }
        return None


class BriefInteractionSerializer(serializers.Serializer):
    """Minimal interaction snapshot for lead detail recent_interactions."""
    id               = serializers.IntegerField()
    type             = serializers.CharField()
    content          = serializers.CharField()
    interaction_date = serializers.DateTimeField()


# ---------------------------------------------------------------------------
# Lead serializers
# ---------------------------------------------------------------------------

class LeadListSerializer(serializers.ModelSerializer):
    """
    Flat, lightweight serializer for GET /api/admin/leads/
    Response shape per Frontend–Backend Contract §7.1
    """

    class Meta:
        model = Lead
        fields = [
            "id",
            "full_name",
            "phone",
            "email",
            "budget_min",
            "budget_max",
            "source",
            "created_at",
        ]


class LeadDetailSerializer(serializers.ModelSerializer):
    """
    Full detail serializer for GET /api/admin/leads/{id}/
    Includes related properties, opportunities (brief), recent interactions.
    Response shape per Frontend–Backend Contract §7.3
    """

    interested_properties = serializers.SerializerMethodField()
    opportunities         = serializers.SerializerMethodField()
    recent_interactions   = serializers.SerializerMethodField()

    class Meta:
        model = Lead
        fields = [
            "id",
            "full_name",
            "phone",
            "email",
            "budget_min",
            "budget_max",
            "preferences",
            "source",
            "interested_properties",
            "opportunities",
            "recent_interactions",
            "created_at",
            "updated_at",
        ]

    def get_interested_properties(self, obj):
        interests = obj.property_interests.select_related("property").all()
        return BriefPropertySerializer(
            [i.property for i in interests], many=True
        ).data

    def get_opportunities(self, obj):
        opps = obj.opportunities.select_related("stage", "property").all()
        return BriefOpportunitySerializer(opps, many=True).data

    def get_recent_interactions(self, obj):
        interactions = obj.interactions.order_by("-interaction_date")[:5]
        return BriefInteractionSerializer(interactions, many=True).data


class LeadCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Used for POST (create) and PATCH (partial update) on leads.
    All writable fields exposed; returns LeadDetailSerializer shape on save.
    """

    class Meta:
        model = Lead
        fields = [
            "full_name",
            "phone",
            "email",
            "budget_min",
            "budget_max",
            "preferences",
            "source",
        ]


# ---------------------------------------------------------------------------
# LeadPropertyInterest serializer
# ---------------------------------------------------------------------------

class LeadPropertyInterestSerializer(serializers.ModelSerializer):
    """
    Used for POST /api/admin/lead-property-interests/
    Accepts: lead_id, property_id, interest_level
    Returns nested lead + property objects per contract §8.1
    """

    lead_id     = serializers.PrimaryKeyRelatedField(
        queryset=Lead.objects.all(), source="lead", write_only=True
    )
    property_id = serializers.PrimaryKeyRelatedField(
        queryset=Property.objects.all(), source="property", write_only=True
    )

    lead     = serializers.SerializerMethodField(read_only=True)
    property = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = LeadPropertyInterest
        fields = [
            "id",
            "lead_id",
            "property_id",
            "lead",
            "property",
            "interest_level",
            "created_at",
        ]

    def validate(self, attrs):
        lead = attrs.get("lead")
        property = attrs.get("property")
        if lead and property:
            if LeadPropertyInterest.objects.filter(lead=lead, property=property).exists():
                raise serializers.ValidationError(
                    {"detail": "This lead is already interested in this property."}
                )
        return attrs

    def get_lead(self, obj):
        return {"id": obj.lead.id, "full_name": obj.lead.full_name}

    def get_property(self, obj):
        return {
            "id": obj.property.id,
            "title_fr": obj.property.title_fr,
            "title_ar": obj.property.title_ar,
        }
