from django.urls import path
from core.views import PublicSettingsView

urlpatterns = [
    path("settings/", PublicSettingsView.as_view(), name="public-settings"),
]
