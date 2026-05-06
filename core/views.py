from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import PublicSettings
from .serializers import PublicSettingsSerializer


class PublicSettingsView(APIView):
    """
    GET /api/public/settings/

    Open endpoint — returns platform-wide public configuration.
    Used by the frontend to get the WhatsApp number and language settings.
    """

    permission_classes = [AllowAny]

    def get(self, request):
        settings = PublicSettings.get()
        serializer = PublicSettingsSerializer(settings)
        return Response(serializer.data)
