import django_filters
from .models import Property


class PropertyFilter(django_filters.FilterSet):
    """
    Filters for public and admin property list endpoints.

    Supported query params:
        search      — not here, handled by SearchFilter in the view
        city        — maps to location_fr (case-insensitive contains)
        type        — exact match (apartment, villa, house, ...)
        min_price   — price >= value
        max_price   — price <= value
        status      — exact match (available, reserved, sold)
        ordering    — handled by OrderingFilter in the view
    """

    city = django_filters.CharFilter(field_name="location_fr", lookup_expr="icontains")
    type = django_filters.ChoiceFilter(choices=Property.Type.choices)
    status = django_filters.ChoiceFilter(choices=Property.Status.choices)
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lte")

    class Meta:
        model = Property
        fields = ["city", "type", "status", "min_price", "max_price"]
