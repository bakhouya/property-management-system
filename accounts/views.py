# =====================================================================================================================
# =====================================================================================================================
from django.forms import ValidationError
from rest_framework import generics, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import AdminUserSerializer, UserListSerializer, CustomLoginUserSerializer
from .models import User
# =====================================================================================================================


# =====================================================================================================================
# This interface handles the login process using APIView in a flexible manner.
# Upon successful authentication, it returns the verification tokens required to access protected interfaces.
# It also returns the login credentials of the user who performed the login.
# =====================================================================================================================
class CustomLoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CustomLoginUserSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response({"error": e.detail}, status=status.HTTP_403_FORBIDDEN if "Blocked" in str(e.detail) else status.HTTP_400_BAD_REQUEST) 
        
        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)

        user_permissions = []
        for group in user.groups.all():
            for permission in group.permissions.all():
                user_permissions.append(permission.codename)

        for permission in user.user_permissions.all():
            user_permissions.append(permission.codename)
        
        user_permissions = list(set(user_permissions))
        # handle response token & data user if auth success
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "phone": user.phone,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "account_type": user.account_type,
                "is_active": user.is_active,
                "is_blocked": user.is_blocked,
                "groups": [group.name for group in user.groups.all()],
                "permissions": user_permissions 
            }
        }, status=status.HTTP_200_OK)
# =====================================================================================================================
# 
# 
# 
# 
# =====================================================================================================================
# This interface is for administrators to create new users.
# Before saving, the account type is set to "admin" to ensure only administrative accounts are created.
# Upon successful operation, the user's data is returned; if errors occur, details of the errors are returned
# =====================================================================================================================
class AdminCreateUserView(generics.CreateAPIView):
    serializer_class = AdminUserSerializer
    
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['account_type'] = 'admin'
        serializer = self.get_serializer(data=data)
        
        if serializer.is_valid():
            user = serializer.save()
            return Response({'user': user}, status=status.HTTP_201_CREATED)
        
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
# =====================================================================================================================
# 
# 
# 
# 
# =====================================================================================================================
# User list display interface with filtering and search support.
# Allows filtering users by account type and status, with the ability to return users associated with a specific group.
# Returns data formatted within a "data" object.
# =====================================================================================================================
class UserListView(generics.ListAPIView):
    serializer_class = UserListSerializer
    queryset = User.objects.all().order_by('-created_at')
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['account_type', 'is_active', 'is_blocked']
    search_fields = ['username', 'email', 'phone', 'first_name', 'last_name']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        group_id = self.request.query_params.get('group_id')
        if group_id:
            queryset = queryset.filter(groups__id=group_id)
    
        return queryset.distinct()

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)        
        return Response({'data': response.data}, status=status.HTTP_200_OK)
# =====================================================================================================================
# 
# 
# 
#  
# =====================================================================================================================
# An interface for permanently deleting a user from the system.
# It extracts the user to be deleted and then executes the deletion process directly.
# It returns a blank response "204" to indicate successful deletion.
# =====================================================================================================================
class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    # permission_classes = [IsAuthenticated, IsAdminUser]  
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user_id = instance.id
        username = instance.username
        
        self.perform_destroy(instance)
        
        return Response(status=status.HTTP_204_NO_CONTENT)
# =====================================================================================================================
# 
# 
# 
# 
# =====================================================================================================================
# Displays details for a single user via ID.
# Uses the UserListSerializer source to return all user data, including groups and permissions.
# Suitable for "User Details" pages within the control panel.
# =====================================================================================================================
class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
# =====================================================================================================================







