from django.contrib import admin

from .models import Lead, LeadPropertyInterest


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display  = ["full_name", "phone", "email", "source", "created_at"]
    list_filter   = ["source"]
    search_fields = ["full_name", "phone", "email"]
    ordering      = ["-created_at"]


@admin.register(LeadPropertyInterest)
class LeadPropertyInterestAdmin(admin.ModelAdmin):
    list_display = ["lead", "property", "interest_level", "created_at"]
    list_filter  = ["interest_level"]
    ordering     = ["-created_at"]
