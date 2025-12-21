from django.forms import ValidationError
from rest_framework import serializers
from accounts.models import User
from chats.rules import MESSAGE_RULES
from utils.validators import DynamicValidator
from .models import Conversation, Message, ImageMessage



# ============================================================================================
# Serializer for users.
# Displays only: ID, username, and avatar.
# ============================================================================================
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        # model = Message._meta.get_field('sender').related_model  
        model = User 
        fields = ['id', 'username', 'avatar']
# ============================================================================================
# 
# 
# ============================================================================================
# Serializer for Image Messages
# This serializer is responsible for handling image messages associated with the message.
# Displays: ID, Image, and Creation Date
# The id and created_at fields are read-only.
# ============================================================================================
class ImageMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageMessage
        fields = ['id', 'image', 'created_at']
        read_only_fields = ['id', 'created_at']
# ============================================================================================




# ============================================================================================
# Message Serializer
# This serializer displays the complete message with sender, recipient, and message images. # All fields are read-only.
# ============================================================================================
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)
    images = ImageMessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'images', 'message', 'video', 'audio', 'is_read', 'created_at']
        read_only_fields = fields
# ============================================================================================
# 
# 
# 
# 
# ============================================================================================
# Serializer for creating or updating messages
# Allows adding multiple images when creating a message
# Includes dynamic validation based on MESSAGE_RULES rules
# ============================================================================================
class MessageCreateOrUpdateSerializer(serializers.ModelSerializer):
    images_files = serializers.ListField(child=serializers.ImageField(), required=False, write_only=True)
    
    class Meta:
        model = Message
        fields = ['id', 'message', 'video', 'audio', 'images', 'sender', 'receiver', "images_files"]
        read_only_fields = ['id', 'images', 'sender', 'receiver',]
    

    # ========================================================================
    # dynamic validator with costom rules 
    def to_internal_value(self, data):
        is_update = self.instance is not None
        validator = DynamicValidator(Message, instance=self.instance if is_update else None)        
        try:
            validation_data = validator.validate(data, MESSAGE_RULES, is_update=is_update)
        except ValidationError as error:
            raise serializers.ValidationError(error.message_dict)
        return super().to_internal_value(validation_data)
    # ========================================================================
    
    # ========================================================================
    # handle create message
    def create(self, data):
        user = self.context['request'].user
        receiver = data['receiver']
        conversation = data['conversation']  
        images_data = data.pop('images_files', [])
        
        # ===== create message
        message = Message.objects.create(
            sender=user,
            receiver=receiver,
            conversation=conversation,
            message=data.get('message'),
            video=data.get('video'),
            audio=data.get('audio')
        )
        
        # ===== save images if has in data
        for image in images_data:
            ImageMessage.objects.create(message=message, image=image)
        
        return message
    # ========================================================================
# ============================================================================================


# ============================================================================================
# Serializer for conversations
# Displays conversation information between sender and receiver
# Includes the number of unread messages and a summary of the last message
# ============================================================================================
class ConversationSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)
    last_message_preview = serializers.CharField(source='last_message', read_only=True)
    unread_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = [
            'id', 'sender', 'receiver', 'last_message_preview',
            'date_last_message', 'is_blocked', 'blocked_by',
            'unread_count', 'created_at'
        ]
        read_only_fields = ['id', 'sender', 'receiver', 'created_at']
    
    def get_unread_count(self, object):
        user = self.context['request'].user
        return Message.objects.filter(conversation=object, receiver=user, is_read=False).count()
# ============================================================================================
# 
# 
# ============================================================================================
# Detailed Serializer for Conversation
# Inherits from ConversationSerializer and displays all fields
# ============================================================================================
class ConversationDetailSerializer(ConversationSerializer):
    class Meta(ConversationSerializer.Meta):
        fields = "__all__"
# ============================================================================================
