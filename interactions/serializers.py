from rest_framework import serializers

from leads.models import Lead
from properties.models import Property
from .models import Interaction


class OpportunityPKField(serializers.PrimaryKeyRelatedField):
    """
    Lazy PrimaryKeyRelatedField for Opportunity.
    Avoids circular import (interactions imports crm, crm imports interactions
    in OpportunityDetailSerializer.get_interactions).
    The queryset is resolved at runtime via get_queryset().
    """

    def get_queryset(self):
        from crm.models import Opportunity
        return Opportunity.objects.all()


class InteractionSerializer(serializers.ModelSerializer):
    """
    Used for list, create, and update on interactions.
    - On READ:  returns nested brief objects for lead, property, opportunity
    - On WRITE: accepts lead_id, property_id, opportunity_id (integer FKs)

    Contract: Frontend–Backend Contract §11
    """

    # Write-only PK inputs
    lead_id        = serializers.PrimaryKeyRelatedField(
        queryset=Lead.objects.all(), source="lead",
        required=False, allow_null=True, write_only=True,
    )
    property_id    = serializers.PrimaryKeyRelatedField(
        queryset=Property.objects.all(), source="property",
        required=False, allow_null=True, write_only=True,
    )
    opportunity_id = OpportunityPKField(
        source="opportunity",
        required=False, allow_null=True, write_only=True,
    )

    # Read-only nested objects
    lead        = serializers.SerializerMethodField(read_only=True)
    property    = serializers.SerializerMethodField(read_only=True)
    opportunity = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Interaction
        fields = [
            "id",
            "type",
            "title",
            "content",
            # write
            "lead_id",
            "property_id",
            "opportunity_id",
            # read
            "lead",
            "property",
            "opportunity",
            "interaction_date",
            "created_at",
        ]

    def get_lead(self, obj):
        if obj.lead:
            return {"id": obj.lead.id, "full_name": obj.lead.full_name}
        return None

    def get_property(self, obj):
        if obj.property:
            return {
                "id": obj.property.id,
                "title_fr": obj.property.title_fr,
                "title_ar": obj.property.title_ar,
            }
        return None

    def get_opportunity(self, obj):
        if obj.opportunity:
            return {"id": obj.opportunity.id}
        return None
