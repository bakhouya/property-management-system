# ========================================================================================
#  Imports requirements
# ========================================================================================
from django.contrib import admin
from django.urls import path, include, re_path
from django.http import JsonResponse
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static
# ========================================================================================
# 
# 
# 
# 
# ========================================================================================
# ========================================================================================
schema_view = get_schema_view(
    openapi.Info(
        title="Property Management System API",
        default_version='v1',
        description="API documentation for the Property Management System",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
# ========================================================================================
# 
# 
# 
# 
# ========================================================================================
# -------- Custom 404 Handler --------
# ========================================================================================
def custom_404(request, exception=None):
    return JsonResponse({
        "status": False,
        "message": "The endpoint you are looking for does not exist."
    }, status=404)
# ========================================================================================
# 
# 
# 
# 
# ========================================================================================
# -------- Project URLs --------
# ========================================================================================
urlpatterns = [
    # ========================================================================================
    # Admin Panel
    path('admin/', admin.site.urls),
    # ========================================================================================



    # ========================================================================================
    # Swagger URLs
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # ========================================================================================

]
# ========================================================================================
# 
# 
# 
# 
# ========================================================================================
# ========================================================================================
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = custom_404
# ========================================================================================

