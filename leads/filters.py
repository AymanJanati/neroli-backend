import django_filters
from .models import Lead


class LeadFilter(django_filters.FilterSet):
    """
    Filters for GET /api/admin/leads/

    Supported query params:
        search   — handled by SearchFilter in the viewset (full_name, phone, email)
        source   — exact match (whatsapp, referral, direct, facebook, instagram, website, other)
        ordering — handled by OrderingFilter in the viewset
    """

    source = django_filters.ChoiceFilter(choices=Lead.Source.choices)

    class Meta:
        model = Lead
        fields = ["source"]
