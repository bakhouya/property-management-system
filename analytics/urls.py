from django.urls import path
from . import views

urlpatterns = [

    path('analytics/dashboard/', views.DailySimpleStatsView.as_view(), name='analytics-summary'),
    path('analytics/visits/source/', views.DetailedSourceAnalysisView.as_view(), name='analytics-summary'),
    

]