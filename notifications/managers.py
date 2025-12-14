from django.db import models


class NotificationManager(models.Manager):

    # =======================================================================================================
    # The appropriate notification message is returned based on the type of notification and the data associated with it.
    # =======================================================================================================
    def _generate_message(self, notification_type, data):
        user = data.get("user", "Someone")
        item_name = data.get("item_name", "")
        action = data.get("action", "") 

        templates = {
            "like": f"{user} liked {item_name}",
            "favorite": f"{user} favorited {item_name}",
            "comment": f"{user} commented on {item_name}",
            "message": f"{user} sent you a new message",
            "block": f"Your property '{item_name}' has been {action} by admin",  
            "unblock": f"Your property '{item_name}' has been {action} by admin",  
            "default": f"You have a new notification from {user}",
        }

        return templates.get(notification_type, templates["default"])
    # =======================================================================================================
    # 
    # 
    # 
    # =======================================================================================================
    # This function is responsible for creating a new notification message based on the called event.
    # It is called when a comment, message, like, or any other type of interaction is created.
    # The function receives the basic data needed to create the notification
    # =======================================================================================================
    def create_notification(self, target_user, action_user, notification_type, **kwargs):
        try:
            if target_user == action_user:
                return False

            NO_DUPLICATE_TYPES = ['like', 'favorite']
            # Extract required fields from keyword arguments
            type_item = kwargs.pop('type_item', None)
            item_id = kwargs.pop('item_id', None)
            item_name = kwargs.pop('item_name', None)
            action = kwargs.pop('action', None)

            if notification_type in NO_DUPLICATE_TYPES:
                if type_item and item_id:
                    from django.utils import timezone
                    from datetime import timedelta
                    time_threshold = timezone.now() - timedelta(hours=24)
                    
                    duplicate_found = self.filter(
                        target_user=target_user,
                        action_user=action_user,
                        type=notification_type,
                        type_item=type_item,
                        item_id=item_id,
                        created_at__gte=time_threshold
                    ).exists()
                    
                    if duplicate_found:
                        return False
            
            # Calling the generate_message function to generate the notification text according to its type and associated data.
            message = self._generate_message(notification_type, {
                'user': action_user.username, 
                'item_name': item_name,
                'action': action
            })
            
            # Create a new notification in the database based on the generated data and the data passed to the function.
            notification = self.create(
                target_user = target_user,
                action_user = action_user,
                type = notification_type,
                type_item = type_item,  
                item_id = item_id,     
                message = message,
                **kwargs
            )
            return {
                'success': True,
                'notification': notification,
                'message': "Notification created successfully"
            }
        except Exception as e:
            return {
                'success': False,
                'notification': None,
                 'message': f'Failed to create notification: {str(e)}'
            }
    # =======================================================================================================
    # 
    # 
    # 
    # =======================================================================================================
    # Notifications are returned for a specific user when that user is the target user in the notification.
    # =======================================================================================================
    def get_user_notifications(self, user):
         queryset = self.filter(target_user=user)
         return queryset
    # =======================================================================================================
    # 
    # 
    # 
    # =======================================================================================================
    # It changes the notification status to "read" when the user interacts with it.
    # =======================================================================================================
    def mark_as_read(self):
        if not self.is_read:
            self.is_read = True
            self.save()
        return self 
    # =======================================================================================================
    # 
    # 
    # 
    # =======================================================================================================
    # A function that returns the number of unread notifications for the target user.
    # =======================================================================================================
    def get_unread_count(self, user):
        return self.filter(target_user=user, is_read=False).count()
    # =======================================================================================================

    