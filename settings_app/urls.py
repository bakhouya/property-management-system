# ============================================================================================
# ============================================================================================
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PlatformSettingsAPIView, MediaSettingsAPIView, SeoSettingsAPIView, SecuritySettingsAPIView, CityViewSet,
    MyUserSettingsView, UserSettingsDetailView, AllUserSettingsListView, AllSettingsAPIView
)


router = DefaultRouter()
router.register(r'cities', CityViewSet, basename='city')


# ============================================================================================
# URL patterns
# ============================================================================================
urlpatterns = [

    path('ad/settings/platform/', PlatformSettingsAPIView.as_view(), name='platform'),
    path('ad/settings/socialmedia/', MediaSettingsAPIView.as_view(), name='social-media'),
    path('ad/settings/seo/', SeoSettingsAPIView.as_view(), name='seo'),
    path('ad/settings/security/', SecuritySettingsAPIView.as_view(), name='security'),

    path('ad/', include(router.urls)),

    # المستخدم يرى ويعدل إعداداته الخاصة 
    path('settings/mysettings/', MyUserSettingsView.as_view(), name='my-user-settings'),    
    # المسؤول يرى ويعدل إعدادات مستخدم معين
    path('ad/settings/user/<uuid:user_id>/', UserSettingsDetailView.as_view(), name='user-settings-detail'),   
    # المسؤول يرى جميع الإعدادات
    path('ad/settings/usersettings/', AllUserSettingsListView.as_view(), name='all-user-settings'),

    path('settings/', AllSettingsAPIView.as_view(), name='all-settings'),
]

# ============================================================================================
# ============================================================================================