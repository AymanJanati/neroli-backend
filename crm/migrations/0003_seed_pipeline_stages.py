"""
Data migration: seed the 8 default pipeline stages.
These are the fixed stages defined in the Backend–Backend Contract §6.3.
This migration runs automatically after 0002_initial.py (which adds FK fields to Opportunity).
"""
from django.db import migrations


PIPELINE_STAGES = [
    {"name": "Nouveau lead",      "slug": "new_lead",      "order": 1},
    {"name": "Contacté",          "slug": "contacted",     "order": 2},
    {"name": "Intéressé",         "slug": "interested",    "order": 3},
    {"name": "Visite planifiée",  "slug": "visit_planned", "order": 4},
    {"name": "Négociation",       "slug": "negotiation",   "order": 5},
    {"name": "Réservé",           "slug": "reserved",      "order": 6},
    {"name": "Vendu",             "slug": "sold",          "order": 7},
    {"name": "Perdu",             "slug": "lost",          "order": 8},
]


def seed_pipeline_stages(apps, schema_editor):
    PipelineStage = apps.get_model("crm", "PipelineStage")
    for stage_data in PIPELINE_STAGES:
        PipelineStage.objects.get_or_create(
            slug=stage_data["slug"],
            defaults={
                "name":  stage_data["name"],
                "order": stage_data["order"],
            },
        )


def unseed_pipeline_stages(apps, schema_editor):
    """Reverse: remove the seeded stages (only removes by slug, preserves custom stages)."""
    PipelineStage = apps.get_model("crm", "PipelineStage")
    slugs = [s["slug"] for s in PIPELINE_STAGES]
    PipelineStage.objects.filter(slug__in=slugs).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("crm", "0002_initial"),
    ]

    operations = [
        migrations.RunPython(seed_pipeline_stages, reverse_code=unseed_pipeline_stages),
    ]
