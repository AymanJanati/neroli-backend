import django_filters
from .models import Interaction


class InteractionFilter(django_filters.FilterSet):
    """
    Filters for GET /api/admin/interactions/

    Supported query params:
        lead        — lead id
        opportunity — opportunity id
        property    — property id
        type        — call, whatsapp, visit, note, other
    """

    lead        = django_filters.NumberFilter(field_name="lead__id")
    opportunity = django_filters.NumberFilter(field_name="opportunity__id")
    property    = django_filters.NumberFilter(field_name="property__id")
    type        = django_filters.ChoiceFilter(choices=Interaction.Type.choices)

    class Meta:
        model = Interaction
        fields = ["lead", "opportunity", "property", "type"]
