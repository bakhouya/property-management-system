from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from .models import User


# =====================================================================================================================
# A source specifically for displaying user data.
# It returns basic user information along with the groups users belong to.
# It also aggregates all permissions derived from groups and individual user permissions.
# This source is for displaying user data and user lists.
# =====================================================================================================================
class UserListSerializer(serializers.ModelSerializer):
    groups = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'first_name', 'last_name', 
                  'account_type', 'is_active', 'is_blocked', 'avatar','date_joined', 'is_staff',
                  'last_login', 'created_at', 'groups', 'permissions'
        ]
    
    def get_groups(self, obj):
        groups = []
        for group in obj.groups.all():
            groups.append({
                'id': group.id,
                'name': group.name,
                'permissions_count': group.permissions.count()
            })
        return groups
    
    def get_permissions(self, obj):
        permissions = set()
        for group in obj.groups.all():
            permissions.update(
                [p.codename for p in group.permissions.all()]
            )
        permissions.update(
            [p.codename for p in obj.user_permissions.all()]
        )
        
        return list(permissions)
# =====================================================================================================================
# 
# 
# 
# 
# =====================================================================================================================
# A dedicated source for creating and updating admin user accounts.
# It verifies passwords before saving and creates the user with all required data.
# When groups are defined, the source automatically assigns them to the user and then gathers all associated permissions.
# These permissions are then added directly to the user to ensure the availability of group-related permissions.
# =====================================================================================================================
class AdminUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'phone', 
            'password', 'confirm_password',
            'first_name', 'last_name', 
            'account_type', 'is_active', 'groups', 'is_staff', 'avatar' 
        ]
    
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({
                'confirm_password': 'كلمات المرور غير متطابقة'
            })
        
        data.pop('confirm_password')
        return data
    
    def create(self, validated_data):
        groups_data = validated_data.pop('groups', None)        
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            account_type=validated_data.get('account_type', 'admin'),
            is_active=validated_data.get('is_active', False),
            is_staff=validated_data.get('is_staff', False),
            avatar=validated_data.get('avatar'),
        )

        user.groups.clear()
        user.user_permissions.clear()

        if groups_data:
            user.groups.set(groups_data)

            all_permissions = set()
            for group in groups_data:
                all_permissions.update(group.permissions.all())
            
            user.user_permissions.add(*all_permissions)
            
        return user
# =====================================================================================================================
# 
# 
# 
#    
# =====================================================================================================================
# This client verifies login credentials via phone number and password.
# It checks the user's presence and the validity of the data, then confirms the account status (activated and not blocked).
# Upon successful verification, it returns the user object within the verified data.
# =====================================================================================================================
class CustomLoginUserSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        phone = data.get("phone")
        password = data.get("password")

        if phone and password:
            user = authenticate(phone=phone, password=password)
            # check if this user exists if not return this meessage
            if not user:
                raise serializers.ValidationError("Invalid phone number or password")
            # check if this user active exists if not return this meessage
            if not user.is_active:
                raise serializers.ValidationError("Your account is deactivated")
            # check if this user not blocked exists if not return this meessage
            if  user.is_blocked:
                raise serializers.ValidationError("Sorry, Your Account Blocked Contact Sepport")
            
        # check if data empty return this message    
        else:
            raise serializers.ValidationError("Phone and password are required")

        data["user"] = user
        return data
# =====================================================================================================================
    






