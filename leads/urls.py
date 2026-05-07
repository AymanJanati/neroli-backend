from rest_framework.routers import DefaultRouter

from .views import LeadPropertyInterestViewSet, LeadViewSet

router = DefaultRouter()
router.register(r"leads", LeadViewSet, basename="lead")
router.register(r"lead-property-interests", LeadPropertyInterestViewSet, basename="lead-property-interest")

urlpatterns = router.urls
