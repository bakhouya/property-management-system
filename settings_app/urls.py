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





# ============================================================================================
# URL patterns
# ============================================================================================
urlpatterns = [
    #  urls platform settings GET & PUT 
    path('ad/settings/platform/', PlatformSettingsAPIView.as_view(), name='platform'),
    #  urls social media settings GET & PUT 
    path('ad/settings/socialmedia/', MediaSettingsAPIView.as_view(), name='social-media'),
    #  urls seo settings GET & PUT 
    path('ad/settings/seo/', SeoSettingsAPIView.as_view(), name='seo'),
    #  urls security settings GET & PUT 
    path('ad/settings/security/', SecuritySettingsAPIView.as_view(), name='security'),

    # include default url to hand GRUD city Model [GET, PUT, PATCH, DELETE, POST] & GET active & POST toggle_status
    path('ad/', include(router.urls)),


    # any personal user can view and update her settings
    path('settings/mysettings/', MyUserSettingsView.as_view(), name='my-user-settings'),    
    # user admin can view and update settings personal user
    path('ad/settings/user/<uuid:user_id>/', UserSettingsDetailView.as_view(), name='user-settings-detail'),   
    # admin user can view all settings personal user
    path('ad/settings/usersettings/', AllUserSettingsListView.as_view(), name='all-user-settings'),
    # get all settings (PlatfromSettings, socialMediaSettings, seoSettings)
    path('settings/', AllSettingsAPIView.as_view(), name='all-settings'),
]

# ============================================================================================
# ============================================================================================