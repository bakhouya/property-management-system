

# ============================================================================================
# ============================================================================================
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
# ============================================================================================



# ============================================================================================
# ============================================================================================
class MaintenanceMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response
        self._maintenance_mode = None
    
    def __call__(self, request):
        path = request.path
        if path.startswith('/api/'):
            if path.startswith('/api/ad/settings/platform/'):
                return self.get_response(request)
            
            if self._check_maintenance_mode():
                return JsonResponse({
                    'maintenance': True,
                    'error': 'SERVICE_UNAVAILABLE',
                    'message': 'System is currently under maintenance.',
                }, status=503)
        
        return self.get_response(request)
    
    def _check_maintenance_mode(self):
        try:
            from settings_app.models import PlatformSettings
            if self._maintenance_mode is None:
                settings = PlatformSettings.get_settings()
                self._maintenance_mode = settings.maintenance_mode
            
            return self._maintenance_mode
            
        except Exception:
            return False
# ============================================================================================
