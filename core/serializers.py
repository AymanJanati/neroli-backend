from rest_framework import serializers
from .models import PublicSettings


class PublicSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicSettings
        fields = [
            "seller_name",
            "whatsapp_phone",
            "default_language",
            "supported_languages",
            "future_languages",
        ]
