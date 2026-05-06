from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Used for /api/auth/me/ and embedded in login response.
    """

    class Meta:
        model = User
        fields = ["id", "full_name", "email", "role"]
        read_only_fields = fields
