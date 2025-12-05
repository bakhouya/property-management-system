import uuid
from django.db import models
from django.conf import settings

# ==========================================================================================================
# This model is designed for user-to-user conversations.
# Each user can communicate with another user.
# Any user can participate in the conversation as either a sender or a receiver.
# ==========================================================================================================
class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='conversations_sender')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='conversations_receiver')

    last_message = models.TextField(null=True, blank=True, verbose_name="Last Message")
    date_last_message = models.DateTimeField(null=True, blank=True, verbose_name="Date of Last Message")

    is_blocked = models.BooleanField(default=False, verbose_name="Is Blocked")
    blocked_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,  null=True, blank=True, related_name='blocked_conversations')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Conversation"
        verbose_name_plural = "Conversations"
        ordering = ['-date_last_message']

        indexes = [
            models.Index(fields=['sender', 'receiver']),
            models.Index(fields=['is_blocked']),
        ]

    def __str__(self):
        return f"Conversation between {self.sender} and {self.receiver}"

    # ==========================================================
    # Toggle Blocking (block/unblock conversation)
    # ==========================================================
    def toggle_block(self, user):
        self.is_blocked = not self.is_blocked
        self.save()
        return self.is_blocked

    # ==========================================================
    # Get user conversations (whether as sender or receiver)
    # ==========================================================
    @classmethod
    def get_user_conversations(cls, user):
        return cls.objects.filter(models.Q(sender=user) | models.Q(receiver=user)).order_by('-date_last_message')
# ==========================================================================================================
# End Conversation Model
# ==========================================================================================================
# 
# 
# 
# 
# 
# ==========================================================================================================
# This module is designed for storing messages between users within a specific conversation.
# A user can be either the sender or the receiver.
# A message may contain only text, text with an image, text with a video, or any combination thereof.
# It allows tracking the read status of each message and the ability to retrieve messages from any conversation.
# ==========================================================================================================
def message_upload_path(instance, filename):
    import os
    ext = os.path.splitext(filename)[1]  
    unique_filename = f"{uuid.uuid4()}{ext}"
    return f"messages/{instance.conversation.id}/{unique_filename}"

class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')   
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')

    message = models.TextField(blank=True, null=True)
    video = models.FileField(upload_to=message_upload_path, blank=True, null=True)
    audio = models.FileField(upload_to=message_upload_path, blank=True, null=True)
    
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['conversation', 'created_at']),
            models.Index(fields=['sender', 'receiver']),
            models.Index(fields=['is_read', 'created_at']),
        ]

    def __str__(self):
        message_preview = self.message[:50] + "..." if self.message and len(self.message) > 50 else self.message           
        return f"From {self.sender.username} to {self.receiver.username}: {message_preview}"

    # ======================================================================================
    # Utility Methods
    # ======================================================================================
    
    
    def mark_as_read(self):
        if not self.is_read:
            self.is_read = True
            self.save()
    
    @classmethod
    def get_conversation_messages(classModel, conversation, limit=50):
        return classModel.objects.filter(conversation=conversation).order_by('created_at')[:limit]
# ==========================================================================================================
# End Message Model
# ==========================================================================================================  
# 
# 
# 
# 
# 
# ==========================================================================================================
# This Model is designed for storing images sent within a single message.
# It allows sending multiple images in one message and separates image management from text messages for increased flexibility.
# Each image is linked to a unique ID to ensure it's organized within a dedicated folder for each message.
# ==========================================================================================================

def image_message_upload_path(instance, filename):
    import os
    ext = os.path.splitext(filename)[1]  
    unique_filename = f"{uuid.uuid4()}{ext}"
    return f"messages/{instance.message.conversation.id}/images/{unique_filename}"

class ImageMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to=image_message_upload_path, blank=True, null=True)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='images')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Image Message"
        verbose_name_plural = "Images Message"
        ordering = ['-created_at']

    def __str__(self):
        return f"Image for message: {self.message.id}"
# ==========================================================================================================
# End ImageMessage Model
# ==========================================================================================================
