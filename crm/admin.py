from django.contrib import admin

from .models import Opportunity, PipelineStage


@admin.register(PipelineStage)
class PipelineStageAdmin(admin.ModelAdmin):
    list_display = ["order", "name", "slug"]
    ordering     = ["order"]


@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display  = ["id", "lead", "property", "stage", "status", "created_at"]
    list_filter   = ["status", "stage"]
    search_fields = ["lead__full_name", "property__title_fr"]
    ordering      = ["-created_at"]
