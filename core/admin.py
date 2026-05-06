from django.contrib import admin
from .models import PublicSettings


@admin.register(PublicSettings)
class PublicSettingsAdmin(admin.ModelAdmin):
    list_display = ["seller_name", "whatsapp_phone", "default_language"]
    
    def has_add_permission(self, request):
        """Prevent creating multiple settings instances; there should be only one."""
        return not PublicSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        """Prevent deleting the singleton instance."""
        return False
