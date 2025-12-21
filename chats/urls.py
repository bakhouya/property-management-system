


from django.urls import path
from . import views

urlpatterns = [
    # View all user conversations
    path('conversations/', views.ConversationListView.as_view(), name='conversation-list'),  
    # Start a new conversation with a specific user or retrieve the conversation if it already exists.
    path('conversations/new/', views.GetOrCreateConversationView.as_view(), name='conversation-with-user'),   
    # Display details of a specific conversation based on the identifier (UUID)
    path('conversations/<uuid:pk>/', views.ConversationDetailView.as_view(), name='conversation-detail'),   
    # Block or unblock a specific conversation
    path('conversations/<uuid:pk>/toggle-block/', views.ToggleBlockConversationView.as_view(), name='conversation-toggle-block'),    
    # Delete conversation
    path('conversations/<uuid:pk>/delete/', views.DeleteConversationView.as_view(), name='conversation-delete'),
    # View specific chat messages or send a new message
    path('conversations/<uuid:conversation_id>/messages/', views.MessageListView.as_view(), name='message-list'),
    # update message
    path('messages/<uuid:pk>/update/', views.MessageUpdateView.as_view(), name='message-update'),
    # delete message
    path('messages/<uuid:pk>/delete/', views.MessageDeleteView.as_view(), name='message-delete'),
    # mark message as read
    path('messages/<uuid:message_id>/read/',  views.MarkMessageReadView.as_view(), name='message-read'),       
]