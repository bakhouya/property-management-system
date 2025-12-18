from django.urls import path
from . import views

urlpatterns = [

    path('analytics/dashboard/', views.DailySimpleStatsView.as_view(), name='analytics-summary'),
    path('analytics/visits/source/', views.DetailedSourceAnalysisView.as_view(), name='analytics-summary'),
    
    # ملخص النظام
    path('analytics/summary/', views.SystemSummaryView.as_view(), name='analytics-summary'),
    
    # إحصائيات العقارات
    path('analytics/properties/stats/', views.PropertyStatsView.as_view(), name='property-stats'),
    
    # إحصائيات المستخدمين
    path('analytics/users/stats/', views.UserStatsView.as_view(), name='user-stats'),
    
    # إحصائيات الزوار
    path('analytics/visitors/stats/', views.VisitorStatsView.as_view(), name='visitor-stats'),
    
    # إحصائيات المحادثات
    path('analytics/conversations/stats/', views.ConversationStatsView.as_view(), name='conversation-stats'),
    
    # إحصائيات حسب الفترة
    path('analytics/period/<str:period>/', views.PeriodStatsView.as_view(), name='period-stats'),
]