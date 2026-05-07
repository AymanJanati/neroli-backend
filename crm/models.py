from django.db import models

from leads.models import Lead
from properties.models import Property


class PipelineStage(models.Model):
    """
    Sales pipeline stage — e.g. new_lead, contacted, interested, ...
    Default stages are seeded via data migration 0002_seed_pipeline_stages.
    Owned by PERSON_B.
    """

    name  = models.CharField(max_length=100)
    slug  = models.SlugField(unique=True)
    order = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name = "Pipeline Stage"
        verbose_name_plural = "Pipeline Stages"
        ordering = ["order"]

    def __str__(self):
        return f"{self.order}. {self.name} ({self.slug})"


class Opportunity(models.Model):
    """
    Sales opportunity linking a Lead to a Property through the pipeline.
    Stage movement triggers property and opportunity status changes.
    Owned by PERSON_B.

    Business rules (move-stage endpoint):
      sold     → opportunity.status = won,  property.status = sold
      lost     → opportunity.status = lost
      reserved → property.status = reserved
      back from sold/reserved → opportunity.status = open; property.status NOT auto-reverted (MVP)
    """

    class Status(models.TextChoices):
        OPEN = "open", "Open"
        WON  = "won",  "Won"
        LOST = "lost", "Lost"

    lead     = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name="opportunities")
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="opportunities")
    stage    = models.ForeignKey(
        PipelineStage,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="opportunities",
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.OPEN,
    )
    notes = models.TextField(blank=True, default="")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Opportunity"
        verbose_name_plural = "Opportunities"
        ordering = ["-created_at"]

    def __str__(self):
        stage_name = self.stage.name if self.stage else "No stage"
        return f"Opp #{self.id} — {self.lead} / {self.property} [{stage_name}]"
