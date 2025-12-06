# ============================================================================================
# Importing packages and core components from Django REST Framework
# ============================================================================================
from rest_framework import viewsets, generics, status, permissions, views
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes

from settings_app.permissions import CanManagePlatformSettings
from .models import (PlatformSettings, SocialMediaSettings, City, SeoSettings, SecuritySettings, UserSettings)

from .serializers import (PlatformSettingsSerializer, SocialMediaSettingsSerializer, SeoSettingsSerializer,
                          SecuritySettingsSerializer, CitySerializer, UserSettingsSerializer, UserSettingsWithUserSerializer)

from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

User = get_user_model()


# ============================================================================================
# Base API View for all settings views
# ============================================================================================
class BaseSettingsAPIView(views.APIView):

    def get_settings_object(self, settings_type):
        return settings_type()
    
    def handle_request(self, request, serializer_class, settings_type, partial=True):
        settings_obj = self.get_settings_object(settings_type)
        
        if request.method == 'GET':
            serializer = serializer_class(settings_obj)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        
        elif request.method in ['PUT']:
            serializer = serializer_class(settings_obj, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)


# ============================================================================================
# Platform Settings API Display 
# Includes (GET – PUT – PATCH) operations for modifying a single element in the settings
# ============================================================================================
class PlatformSettingsAPIView(BaseSettingsAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]  
    def get(self, request):
        return self.handle_request(request, PlatformSettingsSerializer, PlatformSettings.get_settings)
    
    def put(self, request):
        return self.handle_request(request, PlatformSettingsSerializer, PlatformSettings.get_settings)
    
    # def get(self, request):
    #     platform = PlatformSettings.get_settings()
    #     serializer = PlatformSettingsSerializer(platform)
    #     return Response({'data': serializer.data}, status=status.HTTP_200_OK)
    
    # def put(self, request):
    #     platform = PlatformSettings.get_settings()
    #     serializer = PlatformSettingsSerializer(platform, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
       
    #     return Response({'data': serializer.data}, status=status.HTTP_200_OK)
    
    # def patch(self, request):
    #     platform = PlatformSettings.get_settings()
    #     serializer = PlatformSettingsSerializer(platform, data=request.data, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()      
    #     return Response({'data': serializer.data}, status=status.HTTP_200_OK)

# ============================================================================================
# 
# 
# 
# 
# ============================================================================================
# Displaying a dedicated API for managing social media settings – Social Media Settings
# Allows reading and modifying settings (GET – PUT – PATCH)
# ============================================================================================
class MediaSettingsAPIView(BaseSettingsAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request):
        return self.handle_request(request, SocialMediaSettingsSerializer,  SocialMediaSettings.get_social_media_settings)
    
    def put(self, request):
        return self.handle_request(request, SocialMediaSettingsSerializer, SocialMediaSettings.get_social_media_settings)
    
# ============================================================================================
# 
# 
# 
# 
# ============================================================================================
# API Display for SEO Settings
# Allows reading and modifying settings (GET – PUT – PATCH)
# ============================================================================================
class SeoSettingsAPIView(BaseSettingsAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
       
    def get(self, request):
        return self.handle_request(request, SeoSettingsSerializer, SeoSettings.get_seo_settings)
    
    def put(self, request):
        return self.handle_request(request, SeoSettingsSerializer, SeoSettings.get_seo_settings)

# ============================================================================================
# 
# 
# 
# 
# ============================================================================================
# Displays a dedicated API for security settings – Security Settings
# Uses the same algorithm as other settings (GET – PUT – PATCH)
# ============================================================================================
class SecuritySettingsAPIView(BaseSettingsAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    def get(self, request):
        return self.handle_request(request, SecuritySettingsSerializer, SecuritySettings.get_security_settings)
    
    def put(self, request):
        return self.handle_request(request, SecuritySettingsSerializer, SecuritySettings.get_security_settings)

# ============================================================================================
# 
# 
# 
# 
# ============================================================================================
# ViewSet for City Management – ​​Cities
# CRUD provides full functionality, including:
# - List of active cities only
# - Change city status (active/inactive)
# ============================================================================================
class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'active']:
            return [IsAuthenticated()]
        else:
            return [IsAuthenticated(), IsAdminUser()]
        
    @action(detail=False, methods=['get'])
    def active(self, request):
        cities = City.get_active_cities()
        serializer = self.get_serializer(cities, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def toggle_status(self, request, pk=None):
        city = self.get_object()
        city.toggle_status()
        serializer = self.get_serializer(city)

        return Response(serializer.data, status=status.HTTP_200_OK)
# ============================================================================================
# 
# 
# 
# 
# ============================================================================================
# Special offer for current users to read and update their settings – MyUserSettings
# Automatically restores and recreates settings if they are not present.
# ============================================================================================
class MyUserSettingsView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSettingsSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        user_settings, created = UserSettings.objects.get_or_create(user=self.request.user)
       
        return user_settings

    def post(self, request, *args, **kwargs):
        user_settings, created = UserSettings.objects.get_or_create(user=request.user)
        
        serializer = self.get_serializer(user_settings, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({'data': serializer.data }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
# ============================================================================================
# 
# 
# 
# 
# ============================================================================================
# Special offer for administrators to view and update settings for a specific user
# Takes the user_id from the URL and restores its settings
# ============================================================================================
class UserSettingsDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSettingsWithUserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get_object(self):
        user_id = self.kwargs.get('user_id')       
        try:
            user = User.objects.get(id=user_id)
            user_settings, created = UserSettings.objects.get_or_create(user=user)
            return user_settings
        except User.DoesNotExist:
            from rest_framework.exceptions import NotFound
            raise NotFound("User Not Fount")
# ============================================================================================
# 
# 
# 
# 
# ============================================================================================
# Special administrator view to show a list of all user settings
# Uses select_related to optimize queries
# ============================================================================================
class AllUserSettingsListView(generics.ListAPIView):
    serializer_class = UserSettingsWithUserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    pagination_class = None
    
    def get_queryset(self):
        return UserSettings.objects.all().select_related('user')
# ============================================================================================






# ============================================================================================
# Combined All Settings API 
# ============================================================================================
@permission_classes([AllowAny])  
class AllSettingsAPIView(views.APIView):   
    def get(self, request):
        try:

            platform_settings = PlatformSettings.get_settings()
            social_media_settings = SocialMediaSettings.get_social_media_settings()
            active_social_media  = social_media_settings.get_active_social_media()
            seo_settings = SeoSettings.get_seo_settings()
           
            platform_settings_data = PlatformSettingsSerializer(platform_settings)
            seo_settings_data = SeoSettingsSerializer(seo_settings)

            response_data = {"platform":platform_settings_data.data, "social_media": active_social_media, "seo_data": seo_settings_data.data,}
            return Response({"data": response_data}, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"error": {str(e)},}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# ============================================================================================















