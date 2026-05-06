from django.db import models


class PublicSettings(models.Model):
    """
    Singleton model holding platform-wide settings.
    Admin-editable without redeployment.

    There should only ever be ONE row in this table.
    The view always fetches .first().
    """

    class Language(models.TextChoices):
        FR = "fr", "Français"
        AR = "ar", "العربية"

    seller_name = models.CharField(max_length=255, default="CyphX Immobilier")
    whatsapp_phone = models.CharField(
        max_length=30,
        default="+212600000000",
        help_text="International format, e.g. +212600000000",
    )
    default_language = models.CharField(
        max_length=5,
        choices=Language.choices,
        default=Language.FR,
    )
    supported_languages = models.JSONField(
        default=list,
        help_text='JSON array e.g. ["fr", "ar"]',
    )
    future_languages = models.JSONField(
        default=list,
        help_text='Planned languages e.g. ["es"]',
    )

    class Meta:
        verbose_name = "Public Settings"
        verbose_name_plural = "Public Settings"

    def __str__(self):
        return f"PublicSettings — {self.seller_name}"

    def save(self, *args, **kwargs):
        # Enforce singleton — always use pk=1
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        """Helper to always get the singleton, creating if needed."""
        obj, _ = cls.objects.get_or_create(
            pk=1,
            defaults={
                "seller_name": "CyphX Immobilier",
                "whatsapp_phone": "+212600000000",
                "default_language": "fr",
                "supported_languages": ["fr", "ar"],
                "future_languages": ["es"],
            },
        )
        return obj
