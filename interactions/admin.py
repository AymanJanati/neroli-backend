from django.contrib import admin

from .models import Interaction


@admin.register(Interaction)
class InteractionAdmin(admin.ModelAdmin):
    list_display  = ["id", "type", "title", "lead", "interaction_date", "created_at"]
    list_filter   = ["type"]
    search_fields = ["title", "content", "lead__full_name"]
    ordering      = ["-interaction_date"]
