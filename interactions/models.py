from django.db import models

from leads.models import Lead
from properties.models import Property


class Interaction(models.Model):
    """
    A logged interaction or note — call, WhatsApp message, visit, or general note.
    Can be linked to a Lead, a Property, and/or an Opportunity.
    All FK fields are optional so an interaction can be standalone or linked to any combination.
    Owned by PERSON_B.
    """

    class Type(models.TextChoices):
        CALL     = "call",     "Call"
        WHATSAPP = "whatsapp", "WhatsApp"
        VISIT    = "visit",    "Visit"
        NOTE     = "note",     "Note"
        OTHER    = "other",    "Other"

    type    = models.CharField(max_length=20, choices=Type.choices)
    title   = models.CharField(max_length=255)
    content = models.TextField(blank=True, default="")

    # All links are optional — an interaction can be linked to any combination
    lead = models.ForeignKey(
        Lead,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="interactions",
    )
    property = models.ForeignKey(
        Property,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="interactions",
    )
    opportunity = models.ForeignKey(
        "crm.Opportunity",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="interactions",
    )

    interaction_date = models.DateTimeField()
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Interaction"
        verbose_name_plural = "Interactions"
        ordering = ["-interaction_date"]

    def __str__(self):
        lead_name = self.lead.full_name if self.lead else "—"
        return f"[{self.get_type_display()}] {self.title} ({lead_name})"
