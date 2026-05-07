from django.urls import path

from .views import DashboardOverviewView, PipelineSummaryView, RecentActivitiesView

urlpatterns = [
    path("dashboard/overview/",          DashboardOverviewView.as_view(),  name="dashboard-overview"),
    path("dashboard/pipeline-summary/",  PipelineSummaryView.as_view(),    name="dashboard-pipeline-summary"),
    path("dashboard/recent-activities/", RecentActivitiesView.as_view(),   name="dashboard-recent-activities"),
]
