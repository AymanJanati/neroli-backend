from rest_framework.routers import DefaultRouter

from .views import OpportunityViewSet, PipelineStageViewSet

router = DefaultRouter()
router.register(r"pipeline-stages", PipelineStageViewSet, basename="pipeline-stage")
router.register(r"opportunities", OpportunityViewSet, basename="opportunity")

urlpatterns = router.urls
