from django.db import models

from properties.models import Property


class Lead(models.Model):
    """
    Internal lead record — NOT a user account.
    Leads never have passwords, logins, or platform access.
    Owned by PERSON_B.
    """

    class Source(models.TextChoices):
        WHATSAPP  = "whatsapp",  "WhatsApp"
        REFERRAL  = "referral",  "Referral"
        DIRECT    = "direct",    "Direct"
        FACEBOOK  = "facebook",  "Facebook"
        INSTAGRAM = "instagram", "Instagram"
        WEBSITE   = "website",   "Website"
        OTHER     = "other",     "Other"

    full_name   = models.CharField(max_length=255)
    phone       = models.CharField(max_length=30)
    email       = models.EmailField(blank=True, default="")
    budget_min  = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    budget_max  = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    preferences = models.TextField(blank=True, default="")
    source      = models.CharField(
        max_length=20,
        choices=Source.choices,
        default=Source.OTHER,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Lead"
        verbose_name_plural = "Leads"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_name} ({self.phone})"


class LeadPropertyInterest(models.Model):
    """
    Links a lead to a property they are interested in.
    Unique per (lead, property) pair — no duplicates.
    PERSON_B owns this model; PERSON_A's Property is referenced via FK only.
    """

    class Level(models.TextChoices):
        LOW    = "low",    "Low"
        MEDIUM = "medium", "Medium"
        HIGH   = "high",   "High"

    lead     = models.ForeignKey(
        Lead,
        on_delete=models.CASCADE,
        related_name="property_interests",
    )
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="interested_leads",
    )
    interest_level = models.CharField(
        max_length=10,
        choices=Level.choices,
        default=Level.MEDIUM,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Lead–Property Interest"
        verbose_name_plural = "Lead–Property Interests"
        unique_together = ("lead", "property")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.lead} → {self.property} ({self.interest_level})"
