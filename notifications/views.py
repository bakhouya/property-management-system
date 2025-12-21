from rest_framework import generics, permissions, filters
from django.db.models import Q
from notifications.models import Notification
from .serializers import NotificationSerializer

# ==============================================================================
# Get all notification 
# ==============================================================================
class UserNotificationsAPIView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering = ['-created_at']
    
    def get_queryset(self):
        user = self.request.user
        queryset = Notification.objects.filter(target_user=user)

        return queryset
# ==============================================================================
