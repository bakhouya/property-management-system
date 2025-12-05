from venv import logger
from django.contrib import admin
from django.http import JsonResponse
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.core.exceptions import PermissionDenied, BadRequest, ValidationError
from rest_framework.exceptions import APIException, NotFound, ValidationError as DRFValidationError
import logging



def custom_400(request, exception=None):
    error_messages = {
        'BadRequest': 'Bad request. Please check your input.',
        'ValidationError': 'Validation error. Please check your data.',
        'ParseError': 'Error parsing request.',
    }
    
    message = error_messages.get(type(exception).__name__, 'Bad request.')
    
    return JsonResponse({
        "status": False,
        "message": message,
        "error": "400 Bad Request",
        "details": str(exception) if exception else None
    }, status=400)

def custom_403(request, exception=None):
    """Handle 403 Forbidden"""
    return JsonResponse({
        "status": False,
        "message": "You don't have permission to access this resource.",
        "error": "403 Forbidden"
    }, status=403)

def custom_404(request, exception=None):
    """Handle 404 Not Found"""
    return JsonResponse({
        "status": False,
        "message": "The endpoint you are looking for does not exist.",
        "error": "404 Not Found",
        "requested_path": request.path
    }, status=404)

def custom_500(request, *args, **kwargs):
    logger.error(f"500 Error: {kwargs.get('exception', 'Unknown error')}")
    
    return JsonResponse({
        "status": False,
        "message": "Internal server error. Please try again later.",
        "error": "500 Internal Server Error"
    }, status=500)




# ========================================================================================
# Global Exception Handler Middleware (Optional - for more control)
# ========================================================================================
class GlobalExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        # Log the exception
        logger.error(f"Unhandled exception: {type(exception).__name__}: {str(exception)}")
        
        # Handle specific exceptions
        if isinstance(exception, PermissionDenied):
            return custom_403(request, exception)
        
        elif isinstance(exception, (BadRequest, ValidationError)):
            return custom_400(request, exception)
        
        elif isinstance(exception, (NotFound, APIException)):
            # For DRF exceptions
            return JsonResponse({
                "status": False,
                "message": str(exception),
                "error": type(exception).__name__
            }, status=getattr(exception, 'status_code', 500))
        
        # For other unhandled exceptions, return 500
        return custom_500(request, exception=exception)


