from urllib.parse import quote

from rest_framework import serializers

from core.models import PublicSettings
from .models import Property, PropertyImage


# ---------------------------------------------------------------------------
# Image serializer (shared)
# ---------------------------------------------------------------------------

class PropertyImageSerializer(serializers.ModelSerializer):
    """
    Returns { id, url, is_primary }.
    'url' is built from the request context so it's always absolute.
    """

    url = serializers.SerializerMethodField()

    class Meta:
        model = PropertyImage
        fields = ["id", "url", "is_primary"]

    def get_url(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


# ---------------------------------------------------------------------------
# Public serializers
# ---------------------------------------------------------------------------

class PublicPropertyListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for the public property list endpoint.
    Returns only the fields needed for a property card.
    """

    primary_image = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = [
            "id",
            "title_fr",
            "title_ar",
            "type",
            "price",
            "currency",
            "location_fr",
            "location_ar",
            "surface",
            "rooms",
            "status",
            "primary_image",
        ]

    def get_primary_image(self, obj):
        request = self.context.get("request")
        primary = obj.images.filter(is_primary=True).first()
        if not primary:
            primary = obj.images.first()
        if primary and request:
            return request.build_absolute_uri(primary.image.url)
        return None


class PublicPropertyDetailSerializer(serializers.ModelSerializer):
    """
    Full detail serializer for the public property detail page.
    Includes images array and pre-built WhatsApp URLs.
    """

    images = PropertyImageSerializer(many=True, read_only=True)
    whatsapp = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = [
            "id",
            "title_fr",
            "title_ar",
            "type",
            "price",
            "currency",
            "location_fr",
            "location_ar",
            "address_fr",
            "address_ar",
            "surface",
            "rooms",
            "bedrooms",
            "bathrooms",
            "description_fr",
            "description_ar",
            "features_fr",
            "features_ar",
            "status",
            "images",
            "whatsapp",
        ]

    def get_whatsapp(self, obj):
        try:
            settings = PublicSettings.objects.first()
            phone = settings.whatsapp_phone if settings else ""
        except Exception:
            phone = ""

        if not phone:
            return None

        clean_phone = phone.replace("+", "").replace(" ", "")
        base = f"https://wa.me/{clean_phone}"

        msg_contact_fr = f"Bonjour, je suis intéressé par le bien: {obj.title_fr}."
        msg_visit_fr = f"Bonjour, je souhaite demander une visite pour le bien: {obj.title_fr}."
        msg_contact_ar = f"مرحبا، أنا مهتم بهذا العقار: {obj.title_ar}."
        msg_visit_ar = f"مرحبا، أريد طلب زيارة لهذا العقار: {obj.title_ar}."

        return {
            "phone_number": phone,
            "contact_message_fr": msg_contact_fr,
            "visit_message_fr": msg_visit_fr,
            "contact_message_ar": msg_contact_ar,
            "visit_message_ar": msg_visit_ar,
            "contact_url_fr": f"{base}?text={quote(msg_contact_fr)}",
            "visit_url_fr": f"{base}?text={quote(msg_visit_fr)}",
            "contact_url_ar": f"{base}?text={quote(msg_contact_ar)}",
            "visit_url_ar": f"{base}?text={quote(msg_visit_ar)}",
        }


# ---------------------------------------------------------------------------
# Admin serializers
# ---------------------------------------------------------------------------

class AdminPropertyListSerializer(serializers.ModelSerializer):
    """
    For the admin property list — includes timestamps and primary image.
    """

    primary_image = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = [
            "id",
            "title_fr",
            "title_ar",
            "type",
            "price",
            "currency",
            "location_fr",
            "location_ar",
            "surface",
            "rooms",
            "status",
            "primary_image",
            "created_at",
            "updated_at",
        ]

    def get_primary_image(self, obj):
        request = self.context.get("request")
        primary = obj.images.filter(is_primary=True).first()
        if not primary:
            primary = obj.images.first()
        if primary and request:
            return request.build_absolute_uri(primary.image.url)
        return None


class AdminPropertyDetailSerializer(serializers.ModelSerializer):
    """
    Full admin detail — all fields + images array.

    NOTE (Backend–Backend Contract §7.3):
    'interested_leads' is not included here (Option B).
    PERSON_B exposes interested leads via /api/admin/lead-property-interests/
    filtered by property_id. Coordinate with PERSON_B before adding it here.
    """

    images = PropertyImageSerializer(many=True, read_only=True)

    class Meta:
        model = Property
        fields = [
            "id",
            "title_fr",
            "title_ar",
            "type",
            "price",
            "currency",
            "location_fr",
            "location_ar",
            "address_fr",
            "address_ar",
            "surface",
            "rooms",
            "bedrooms",
            "bathrooms",
            "description_fr",
            "description_ar",
            "features_fr",
            "features_ar",
            "status",
            "is_public",
            "images",
            "created_at",
            "updated_at",
        ]


class PropertyCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Used for POST (create) and PATCH (partial update) on admin properties.
    All fields are writable. Returns AdminPropertyDetailSerializer shape on save.
    """

    class Meta:
        model = Property
        fields = [
            "title_fr",
            "title_ar",
            "type",
            "price",
            "currency",
            "location_fr",
            "location_ar",
            "address_fr",
            "address_ar",
            "surface",
            "rooms",
            "bedrooms",
            "bathrooms",
            "description_fr",
            "description_ar",
            "features_fr",
            "features_ar",
            "status",
            "is_public",
        ]
