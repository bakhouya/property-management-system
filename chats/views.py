from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .models import Conversation, Message
from .serializers import (ConversationSerializer, ConversationDetailSerializer, MessageCreateOrUpdateSerializer, MessageSerializer)
from .permissions import IsParticipant, IsReceiver, IsSender
from django.contrib.auth import get_user_model
User = get_user_model()


# ============================================================================================================
# In this section, we retrieve all conversations associated with the user who made the request,
# whether that user is the sender or receiver within the conversation.

# A fundamental requirement is to return only conversations containing actual messages,
# to avoid displaying empty conversations in which no messages have yet been exchanged.

# This logic aims to:
# - Improve the user experience by not displaying unused conversations
# - Prevent the other party from seeing a conversation if it was created but no message was sent
# - Ensure that every conversation displayed has involved real interaction between the two parties
# # The end result:
# The user receives a list of only active conversations in which they have actually participated, either as a sender or receiver.

# =========================================================================================================
class ConversationListView(generics.ListAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        queryset = Conversation.get_user_conversations(user)
        queryset = queryset.filter(last_message__isnull=False).order_by('-date_last_message')
        return queryset
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
# ================================================================
# 
# 
# ============================================================================================================
# In this part of the code, we create a new conversation or retrieve an existing one,
# between the user who sent the request and the user they chose to communicate with.
# # First, we check if there is a previous conversation between the two parties,
# whether the current user is the sender or the receiver in that conversation.
# #
# If an existing conversation is found:
# - The same conversation is returned without creating a new record in the database.
# - This prevents duplicate conversations between the same users.
# # If no previous conversation exists:
# - A new conversation is created between the users.
# - It is correctly linked to both parties (sender/receiver).
# # The purpose of this logic is:
# - To ensure there is only one conversation between each pair of users.
# - To maintain data organization and prevent unnecessary duplication.
# - To improve the user experience when starting or completing conversations.
# =========================================================================================================
class GetOrCreateConversationView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user_id = request.query_params.get('user_id')
        
        if not user_id:
            return Response({'error': 'reciver key not sended in url'}, status=status.HTTP_400_BAD_REQUEST)
       
        try:
            other_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'user not exists'}, status=status.HTTP_404_NOT_FOUND)
               
        if other_user == request.user:
            return Response({'error': 'you can not create conversation with yourself'}, status=status.HTTP_400_BAD_REQUEST)
        
        # check if elready has conversation between this two users [other_user & request.user] 
        conversation = Conversation.objects.filter(
            (Q(sender=request.user) & Q(receiver=other_user)) |
            (Q(sender=other_user) & Q(receiver=request.user))
        ).first()
        
        # if not create new conversation
        if not conversation:
            conversation = Conversation.objects.create(sender=request.user, receiver=other_user)
        
        serializer = ConversationDetailSerializer(
            conversation,
            context={'request': request}
        )
        return Response(serializer.data)
# ================================================================
# 
# 
# ======================================================================================================
# In this section, we are returning details for only one conversation,
# ======================================================================================================
class ConversationDetailView(generics.RetrieveAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipant]
    queryset = Conversation.objects.all()
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
# ================================================================
# 
# 
# ========================================================================================================
# In this section, we toggle the chat blocking status.
# If the chat is not blocked, it is blocked; if it is blocked, it is unblocked.
# We also update the blocked_by field to identify the user who initiated the block.
# =========================================================================================================
class ToggleBlockConversationView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsParticipant]
    
    def post(self, request, pk):
        conversation = get_object_or_404(Conversation, id=pk)
        self.check_object_permissions(request, conversation)
        is_blocked = conversation.toggle_block(request.user)
        # update field blocked_by 
        conversation.blocked_by = request.user if is_blocked else None
        conversation.save()
        
        return Response({'id': conversation.id, 'is_blocked': conversation.is_blocked})
# ================================================================
# 
# 
# =========================================================================================================
# In this section, we delete the conversation.
# This process is only permitted for members participating in this conversation,
# to ensure that no unauthorized user can delete a conversation that does not belong to them.
# =========================================================================================================
class DeleteConversationView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsParticipant]
    queryset = Conversation.objects.all()
    
    def perform_destroy(self, instance):
        instance.delete()
# ================================================================
# 
# 
# =========================================================================================================
# This View is responsible for:
# 1 Fetching all messages in a given conversation (GET)
# 2 Creating a new message within the same conversation (POST)
#
# Permissions:
# - The user must be logged in
# - The user must be a participant in the conversation (sender or recipient)
#
# When fetching messages:
# - The user is first verified to be participating in the conversation
# - All messages in the conversation are returned in order of creation date
# - Images associated with messages are loaded using prefetch_related to improve performance
#
# When creating a new message:
# - The recipient is automatically determined based on the other participant in the conversation
# - The message is saved and linked to the conversation
# - The last message in the conversation table (last_message) is updated
# - The date of the last message is updated (date_last_message)
# =========================================================================================================================
class MessageListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsParticipant]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return MessageCreateOrUpdateSerializer
        return MessageSerializer
    
    def get_queryset(self):
        conversation_id = self.kwargs['conversation_id']
        conversation = get_object_or_404(Conversation, id=conversation_id)
        # check if user is participant in this conversation
        if self.request.user not in [conversation.sender, conversation.receiver]:
            self.permission_denied(self.request)
        
        # get all message conversation with images if has
        return Message.objects.filter(conversation=conversation).prefetch_related('images').order_by('created_at')
    
    def perform_create(self, serializer):
        #  handle data requiement
        conversation_id = self.kwargs['conversation_id']
        # get conversation id
        conversation = get_object_or_404(Conversation, id=conversation_id)
        current_user = self.request.user
        # handle receiver and sender
        if current_user == conversation.sender:
            receiver = conversation.receiver
        else:
            receiver = conversation.sender
    
        message = serializer.save(sender = self.request.user, receiver=receiver, conversation = conversation)
        
        # update conversation last message and date_last_message 
        conversation.last_message = message.message[:100] if message.message else "Image"
        conversation.date_last_message = message.created_at
        conversation.save()
# ================================================================
# 
# 
# =========================================================================================================
# This View is responsible for:
#   Editing an existing message within the conversation
#
#   Permissions:
    # - The user must be logged in
    # - Editing is only permitted for the message sender (IsSender)
# =========================================================================================================
class MessageUpdateView(generics.UpdateAPIView):
    serializer_class = MessageCreateOrUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsSender]
    queryset = Message.objects.all()
    
    def perform_update(self, serializer):
        serializer.save()
# ================================================================
# 
# 
# =========================================================================================================
# Remove a message from the conversation
# Permissions: 
#  - the user must be logged in 
#  - deletion in only allowed for the message sender (IsSender)
# =========================================================================================================
class MessageDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsSender]
    queryset = Message.objects.all()
# ================================================================
# 
# 
# ============================================================================================================
# This View is responsible for:
# > Marking the message as Read
#
# > Permissions:
# - The user must be logged in
# - Only the message recipient (IsReceiver) is allowed to perform the operation
#
# > Security Notes:
# - Even if the user is participating in the conversation, they cannot mark the message as read
# unless they are the actual recipient
# - This is verified twice: via a custom permission + a condition within the View
#
# > How it works:
# 1️ The message is fetched based on the message_id
# 2️ The current user is verified as the message recipient
# 3️ The message status is updated to "Read"
# 4️ Message status is restored after refresh
#
# > Objective:
# To ensure readability and prevent any tampering with message status
# =========================================================================================================
class MarkMessageReadView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsReceiver]
    
    def post(self, request, message_id):
        message = get_object_or_404(Message, id=message_id)
        if message.receiver != request.user:
            return Response({'error': 'Just Receiver can read message'}, status=status.HTTP_403_FORBIDDEN)
        
        message.mark_as_read()
        return Response({'id': message.id, 'is_read': message.is_read})
# ================================================================

