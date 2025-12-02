import uuid
from django.db import models
from django.conf import settings
from .managers import NotificationManager

# ==============================================================================
# Model Notification 
# ==============================================================================
class Notification(models.Model):
    # This unique field distinguishes each element from the other with a special identifier.
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # This field is for specifying the user who will receive the notification,
    # so that the system can accurately direct alerts only to the user concerned.
    target_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications', verbose_name="Target User")
    
    # This field is for identifying the user who sent the notification,
    # such as the user who liked or added a comment, in order to link the notification to the action that was performed.
    action_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_notifications', verbose_name="Action User")
    
    # This field specifies the type of notification directed to the user, such as: comment, like, message or others.
    NOTIFICATION_TYPES = [('like', 'Like'), ('comment', 'Comment'), ('message', 'Message')]
    type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, verbose_name="Notification Type")
    
    # This field specifies the type of item associated with the notification, such as property, message, or other.
    type_item = models.CharField(max_length=100, blank=True, null=True, verbose_name="Item Type")
    # It is designated to store the ID of the item associated with the notification; for example, 
    # when a notification is related to a property, the ID number of that property is placed here.
    item_id = models.UUIDField(blank=True, null=True, verbose_name="Item ID")

    is_read = models.BooleanField(default=False, verbose_name="Is Read")
    message = models.TextField(blank=True, null=True, verbose_name="Notification Message")
      
    created_at = models.DateTimeField(auto_now_add=True)


    # call class object 
    objects = NotificationManager()


    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['target_user', 'is_read']),
            models.Index(fields=['type', 'created_at']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.type} notification for {self.target_user.username} from {self.action_user.username}"
# ==============================================================================

