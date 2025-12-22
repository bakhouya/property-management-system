# =====================================================================================================================
# =====================================================================================================================
from django.forms import ValidationError
from rest_framework import generics, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.paginations import CustomPagination
from rest_framework_simplejwt.tokens import RefreshToken

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
# import permissions class
from .permissions import (CanViewUser, CanChangeUser, CanActivateUser, CanDeleteUser, 
                          CanListUsers, CanAddUser)

# imports serializers classes
from .serializers import AdminUserSerializer, CustomLoginUserSerializer, PersonalRegisterSerializer, ProfileSerializer
# import model class 
# from .models import User
# import filter class
from .filters import UserFilter
from django.contrib.auth import get_user_model
User = get_user_model()
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
                "avatar": user.avatar.url if user.avatar and user.avatar.name else None,
                "phone": user.phone,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "account_type": user.account_type,
                "is_staff": user.is_staff,
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
# permissions required : AUTH, ADMIN, CAN CREATE USER
# =====================================================================================================================
class AdminCreateUserView(generics.CreateAPIView):
    serializer_class = AdminUserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser, CanAddUser]
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['account_type'] = 'admin'
        serializer = self.get_serializer(data=data)
        
        if serializer.is_valid():
            user = serializer.save()
            return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# =====================================================================================================================
# 
# 
# 
# 
# =====================================================================================================================
# Update user interface
# permissions required : AUTH, ADMIN, CAN UPDATE USER
# =====================================================================================================================
class AdminUpdateUserView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser, CanChangeUser]

    def get_queryset(self):
        return User.objects.prefetch_related('groups__permissions','user_permissions').all()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        
        if serializer.is_valid():
            user = serializer.save()
 
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# =====================================================================================================================
# 
# 
# 
# 
# =====================================================================================================================
# User list display interface with filtering and search support.
# Allows filtering users by account type and status, with the ability to return users associated with a specific group.
# Returns data formatted within a "data" object.
# permissions required : AUTH, ADMIN, CAN VIEW LIST USERS
# =====================================================================================================================
class UserListView(generics.ListAPIView):
    serializer_class = AdminUserSerializer 
    permission_classes = [IsAuthenticated, IsAdminUser, CanListUsers] 
    queryset = User.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username', 'email', 'phone', 'first_name', 'last_name']
    filterset_class = UserFilter
    ordering = ['-created_at']
    ordering_fields = ['created_at', 'username', 'email', 'first_name', 'last_name']
    pagination_class = CustomPagination
    
    
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
# permissions required : AUTH, ADMIN, CAN DELETE USER
# =====================================================================================================================
class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser, CanDeleteUser]  
    
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
# permissions required : AUTH, ADMIN, CAN VIEW USER
# =====================================================================================================================
class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = [IsAuthenticated, CanViewUser] 

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
# =====================================================================================================================
# 
# 
# 
#  
# =====================================================================================================================
# Here, we enable the user to change the status of other users using the "toggle" feature.
# However, this process is not open to everyone:
    # - The user must be logged in.
    # - They must have specific permissions (can_activate_user).
    # - A regular admin user does not have the right to control a superuser or change their status.
# The purpose of this condition is to protect sensitive accounts (like superusers) and prevent any unauthorized modifications.
# permissions required : AUTH, ADMIN, CAN ACTIVATE USER
# =====================================================================================================================
class ToggleStatusUser(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser, CanActivateUser]
    
    def post(self, request, *args, **kwargs):
        user = self.get_object()
        
        if user.is_superuser and not request.user.is_superuser:
            return Response({'error': 'You cannot disable a user with higher privileges than yours'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            user = user.toggle_status()
            serializer = self.get_serializer(user)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
            
        except Exception as error:
            return Response({'error': f'  Change user not successfully: {str(error)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# =====================================================================================================================





# =====================================================================================================================
# This section allows anyone to register a new account directly (registration is open).
# However, there is a key condition:
    # - The user who registers this way does not have any groups or permissions.
    # - This confirms that the account registered here is a regular user account and not an administrator account.
    # - It is not necessary to be logged in to register; registration is open to everyone.
# Result:
    # - Any user who registers from this point forward → is considered a "regular user" without administrative privileges.
    # - Once registration is successful, their data is returned along with a validated token (JWT) so they can use the protected interfaces that require login.
# The purpose of this condition is to separate administrative accounts (admin/superuser) that are managed internally, and regular accounts that anyone can create through the registration interface.
# =====================================================================================================================
class PersonalRegisterView(generics.CreateAPIView):
    serializer_class = PersonalRegisterSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            response_data = serializer.data
            
            return Response({'data': response_data}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# =====================================================================================================================
# 
# 
# 
#    
# =====================================================================================================================
# This interface is responsible for displaying the profile data of any registered user, allowing them to view and update their information.
# Any user has the right to view their profile and modify personal data (such as name, phone number, email address, etc.).
# However, when we perform an update, we only allow the updating of basic data.
# Sensitive fields such as:
    # * groups
    # * is_active (Account activation/deactivation)
    # * is_staff (Administrative permissions)
# These cannot be changed by the user, whether it's a personal account or a regular admin account.
# The purpose of this condition is to:
# Protect system permissions from any unauthorized modification.
# Let the user control only their personal data without tampering with sensitive fields that affect public security.
# =====================================================================================================================
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]  
    
    def get_object(self):
        return self.request.user
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
# =====================================================================================================================




