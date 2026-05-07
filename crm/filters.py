import django_filters
from .models import Opportunity


class OpportunityFilter(django_filters.FilterSet):
    """
    Filters for GET /api/admin/opportunities/

    Supported query params:
        stage    — stage slug (e.g. interested, negotiation)
        status   — open, won, lost
        lead     — lead id
        property — property id
    """

    stage    = django_filters.CharFilter(field_name="stage__slug", lookup_expr="exact")
    status   = django_filters.ChoiceFilter(choices=Opportunity.Status.choices)
    lead     = django_filters.NumberFilter(field_name="lead__id")
    property = django_filters.NumberFilter(field_name="property__id")

    class Meta:
        model = Opportunity
        fields = ["stage", "status", "lead", "property"]
