from django.db.models import Count, Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from crm.models import Opportunity, PipelineStage
from crm.serializers import PipelineStageSerializer
from interactions.models import Interaction
from leads.models import Lead
from properties.models import Property


class DashboardOverviewView(APIView):
    """
    GET /api/admin/dashboard/overview/

    Returns aggregated counts for properties, leads, and opportunities.
    Response shape per Frontend–Backend Contract §12.1

    'leads.active' = leads that have at least one open opportunity.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Property counts
        prop_qs = Property.objects.values("status").annotate(count=Count("id"))
        prop_counts = {row["status"]: row["count"] for row in prop_qs}

        # Lead counts
        total_leads  = Lead.objects.count()
        active_leads = Lead.objects.filter(
            opportunities__status=Opportunity.Status.OPEN
        ).distinct().count()

        # Opportunity counts
        opp_qs = Opportunity.objects.values("status").annotate(count=Count("id"))
        opp_counts  = {row["status"]: row["count"] for row in opp_qs}
        total_opps  = Opportunity.objects.count()

        return Response({
            "properties": {
                "total":     Property.objects.count(),
                "available": prop_counts.get("available", 0),
                "reserved":  prop_counts.get("reserved",  0),
                "sold":      prop_counts.get("sold",       0),
            },
            "leads": {
                "total":  total_leads,
                "active": active_leads,
            },
            "opportunities": {
                "total": total_opps,
                "open":  opp_counts.get("open", 0),
                "won":   opp_counts.get("won",  0),
                "lost":  opp_counts.get("lost", 0),
            },
        })


class PipelineSummaryView(APIView):
    """
    GET /api/admin/dashboard/pipeline-summary/

    Returns opportunity count per pipeline stage (open opportunities only).
    Response shape per Frontend–Backend Contract §12.2
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        stages = PipelineStage.objects.all()

        # Count open opportunities per stage in a single query
        stage_counts = {
            row["stage_id"]: row["count"]
            for row in Opportunity.objects.filter(status=Opportunity.Status.OPEN)
            .values("stage_id")
            .annotate(count=Count("id"))
        }

        result = [
            {
                "stage": PipelineStageSerializer(stage).data,
                "count": stage_counts.get(stage.id, 0),
            }
            for stage in stages
        ]
        return Response(result)


class RecentActivitiesView(APIView):
    """
    GET /api/admin/dashboard/recent-activities/

    Returns latest 20 interactions ordered by most recent interaction_date.
    Response shape per Frontend–Backend Contract §12.3
    Optional for MVP — included for completeness.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        interactions = Interaction.objects.select_related("lead").order_by(
            "-interaction_date"
        )[:20]

        result = [
            {
                "id":          i.id,
                "type":        "interaction",
                "title":       i.title,
                "description": i.content,
                "created_at":  i.created_at,
            }
            for i in interactions
        ]
        return Response(result)
