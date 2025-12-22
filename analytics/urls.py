
from django.urls import path
from .views import DetailedSourceAnalysisView, SimpleDashboardStatsAPIView, VisitStatsAPIView

urlpatterns = [
    path('analytics/visists/sources/', DetailedSourceAnalysisView.as_view(), name='detailed-source-analysis'),
    path('dashboard/simple-stats/', SimpleDashboardStatsAPIView.as_view(), name='simple-dashboard-stats'),
    path('stats/visits/', VisitStatsAPIView.as_view(), name='visit-stats'),
]