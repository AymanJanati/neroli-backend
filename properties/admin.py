from django.contrib import admin
from .models import Property, PropertyImage


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1
    readonly_fields = ["created_at"]
    fields = ["image", "is_primary", "created_at"]


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ["title_fr", "type", "status", "price", "currency", "location_fr", "is_public", "created_at"]
    list_filter = ["type", "status", "is_public", "currency"]
    search_fields = ["title_fr", "title_ar", "location_fr", "location_ar"]
    ordering = ["-created_at"]
    inlines = [PropertyImageInline]
    readonly_fields = ["created_at", "updated_at"]

    fieldsets = (
        ("French Content", {
            "fields": ("title_fr", "description_fr", "features_fr", "location_fr", "address_fr")
        }),
        ("Arabic Content", {
            "fields": ("title_ar", "description_ar", "features_ar", "location_ar", "address_ar")
        }),
        ("Property Details", {
            "fields": ("type", "status", "price", "currency", "surface", "rooms", "bedrooms", "bathrooms", "is_public")
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at")
        }),
    )


@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ["property", "is_primary", "created_at"]
    list_filter = ["is_primary"]
    readonly_fields = ["created_at"]
