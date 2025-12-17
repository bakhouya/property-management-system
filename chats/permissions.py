from rest_framework.permissions import BasePermission

class IsParticipant(BasePermission):
    """
    صلاحية للتأكد أن المستخدم مشارك في المحادثة
    """
    def has_object_permission(self, request, view, obj):
        # للرسائل: تأكد أن المستخدم هو المرسل أو المستقبل
        if hasattr(obj, 'conversation'):
            conversation = obj.conversation
        else:
            conversation = obj
        
        return request.user in [conversation.sender, conversation.receiver]

class IsSender(BasePermission):
    """
    صلاحية للتأكد أن المستخدم هو مرسل الرسالة
    """
    def has_object_permission(self, request, view, obj):
        return obj.sender == request.user

class IsReceiver(BasePermission):
    """
    صلاحية للتأكد أن المستخدم هو مستقبل الرسالة
    """
    def has_object_permission(self, request, view, obj):
        return obj.receiver == request.user