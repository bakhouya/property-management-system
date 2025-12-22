
from django.forms import ValidationError
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate
from .models import User
from utils.validators import DynamicValidator
from utils.helpers import handle_file_update
from .rules import USER_RULES
from rest_framework_simplejwt.tokens import RefreshToken

# =====================================================================================================================
# A dedicated source for creating and updating admin user accounts.
# It verifies passwords before saving and creates the user with all required data.
# When groups are defined, the source automatically assigns them to the user and then gathers all associated permissions.
# These permissions are then added directly to the user to ensure the availability of group-related permissions.
# =====================================================================================================================
class AdminUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password], style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    groups = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), many=True, required=False)
    groups_user = serializers.SerializerMethodField(read_only=True)
    permissions = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id',
            'username', 'email', 'phone', 
            'password', 'confirm_password',
            'first_name', 'last_name', 
            'account_type', 'is_active', 'groups', 'is_staff', 'avatar', 'permissions', 'groups_user',
        ]
        read_only_fields = ['permissions', 'groups_user', 'created_at', 'updated_at']
        extra_kwargs = {'password': {'write_only': True}, 'confirm_password': {'write_only': True}}

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields['password'].required = False
            self.fields['confirm_password'].required = False

    # =========================================================================================================================================
    # This function calls the dynamic validation system before performing default DRF checks.
    # It relies on an external class in "utils/validators.py" to implement custom validation rules.
    # The goal is to add an extra, customizable validation layer before proceeding to the serializer's regular validation.
    # =========================================================================================================================================
    def to_internal_value(self, data):
        validator = DynamicValidator(User, instance=self.instance)
        is_update = self.instance is not None
        try:
            cleaned_data = validator.validate(data, USER_RULES, is_update=is_update)
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)

        return super().to_internal_value(cleaned_data)
    # =========================================================================================================================================
    #  
    # 
    # 
    # 
    # =========================================================================================================================================
    # This function checks if the password matches the confirmation before proceeding with the verification process.
    # If there is a mismatch, an error is raised and the saving process is stopped.
    # It aims to ensure that correct and matching passwords are entered.
    # =========================================================================================================================================
    def validate(self, data):
        if 'password' in data or 'confirm_password' in data:
            if data.get('password') != data.get('confirm_password'):
               raise serializers.ValidationError({'error': 'Password does not match confirmation'})
        return data
    # =========================================================================================================================================
    #  
    # 
    # 
    # 
    # =========================================================================================================================================
    # get all groups info for this user
    # =========================================================================================================================================
    def get_groups_user(self, obj):
        groups_data = []
        for group in obj.groups.all():
            groups_data.append({
                'id': group.id,
                'name': group.name,
                # 'permissions': [perm.codename for perm in group.permissions.all()]
            })
        return groups_data
    # =========================================================================================================================================
    #  
    # 
    # 
    # 
    # =========================================================================================================================================
    # get all permisions info for this user
    # =========================================================================================================================================    
    def get_permissions(self, obj):
        user_permissions = []
        
        for group in obj.groups.all():
            for permission in group.permissions.all():
                full_perm = f"{permission.content_type.app_label}.{permission.codename}"
                user_permissions.append(full_perm)
        
        for permission in obj.user_permissions.all():
            full_perm = f"{permission.content_type.app_label}.{permission.codename}"
            user_permissions.append(full_perm)
        
        return list(set(user_permissions))
    # 
    # 
    # 
    # 
    # =========================================================================================================================================
    # handle create new user from admin with groups and permissions
    # =========================================================================================================================================
    def create(self, validated_data):
        # Extracting the sent groups (if any) from the verified data
        groups_data = validated_data.pop('groups', None)  
        # Create a new user using the required fields
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            account_type=validated_data.get('account_type', 'admin'),
            is_active=validated_data.get('is_active', False),
            is_staff=validated_data.get('is_staff', True),
            avatar=validated_data.get('avatar'),
        )
        # Ensure that the new user does not inherit any old groups or permissions
        user.groups.clear()
        user.user_permissions.clear()
        # If there are groups, assign them and collect their permissions
        if groups_data:
            # get this groups to user
            user.groups.set(groups_data)
            # get all permissions from this groups
            all_permissions = set()
            for group in groups_data:
                all_permissions.update(group.permissions.all()) 
            # get this permissions to user    
            user.user_permissions.add(*all_permissions)            
       
        return user
     #  
    # =========================================================================================================================================
    # 
    # 
    #   
    # =========================================================================================================================================
    # handle  update user from admin with groups and permissions
    # =========================================================================================================================================
    def update(self, instance, validated_data):
        # Extracting the sent groups, password, confirm_password from the verified data
        # for updated user we can't updated the password 
        validated_data.pop('password', None)
        validated_data.pop('confirm_password', None)
        groups_data = validated_data.pop('groups', None)
        # if user update avatar profile we call handle_file_update from "utils/helpers"
        # this method handle if user updated avatar we delete old image from static file
        if "avatar" in validated_data:
            handle_file_update(validated_data.get("avatar"), instance.avatar)
         # Create a new user using the required fields   
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        # if user update groups 
        if groups_data is not None:
            # clean old groups for this user and get new groups for him
            instance.groups.clear()
            instance.groups.set(groups_data)
            # clean old permissions for this user and get new for him          
            instance.user_permissions.clear()
            all_permissions = set()
            for group in groups_data:
                all_permissions.update(group.permissions.all())
            
            instance.user_permissions.add(*all_permissions)
        
        return instance
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
                raise serializers.ValidationError({"error": "Invalid phone number or password"})
            # check if this user active exists if not return this meessage
            if not user.is_active:
                raise serializers.ValidationError({"error": "Your account is deactivated"})
            # check if this user not blocked exists if not return this meessage
            if  user.is_blocked:
                raise serializers.ValidationError({"error": "Sorry, Your Account Blocked Contact Sepport"})
            
        # check if data empty return this message    
        else:
            raise serializers.ValidationError({"error": "Invalid phone number or password"})

        data["user"] = user
        return data
# =====================================================================================================================
# 
# 
# 
#    
# =====================================================================================================================
# Personal Register Serializer 
# =====================================================================================================================
class PersonalRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password], style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'phone', 'password', 'confirm_password', 'first_name', 'last_name', "visitor", "is_staff", "is_active", "account_type", "avatar"
        ]
        read_only_fields = ['id', "is_staff", "is_active", "account_type", "created_at", "updated_at", "avatar"]
        extra_kwargs = {
            'password': {'write_only': True},
            'confirm_password': {'write_only': True}
        }
    
    # =====================================================================
    # Dynamic validation
    # =====================================================================
    def to_internal_value(self, data):
        validator = DynamicValidator(User, instance=None)
        is_update = False          
        try:
            cleaned_data = validator.validate(data, USER_RULES, is_update=is_update)
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)
        return super().to_internal_value(cleaned_data)
    
    # =====================================================================
    # Validatio defaut
    # =====================================================================
    def validate(self, data):
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError({'error': 'Password does not match confirmation'})
        return data
    
    # =====================================================================
    # create pesonal account user  
    # =====================================================================
    def create(self, validated_data):
        validated_data.pop('confirm_password', None)

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            visitor=validated_data.get('visitor'),
            
            is_superuser=False,
            account_type='personal', 
            is_staff=False,      
            is_active=True,          
        )
    
        user.groups.clear()
        user.user_permissions.clear()
        
        return user
    
    # =====================================================================
    # representation return data with jwt tokens
    # =====================================================================
    def to_representation(self, instance):

        refresh = RefreshToken.for_user(instance)
        
        representation = {
            'user': {
                'id': instance.id,
                'username': instance.username,
                'email': instance.email,
                'phone': instance.phone,
                "avatar": instance.avatar.url if instance.avatar and instance.avatar.name else None,
                'first_name': instance.first_name,
                'last_name': instance.last_name,
                'account_type': instance.account_type,
                'is_staff': instance.is_staff,
                'is_active': instance.is_active,
                'visitor': instance.visitor,
                'created_at': instance.created_at,
                'updated_at': instance.updated_at,
            },
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }
        
        return representation
# =====================================================================================================================
# 
# 
# 
# 
# =====================================================================================================================
# This Serializer is for the profile of any registered user.
    # - It allows the user to see their personal data (ID, username, email, phone, first name, last name, avatar, etc.).
    # - Sensitive fields such as account_type, is_active, is_staff, groups, and permissions are only read-only.
# This means the user cannot change them themselves to protect the system from any unauthorized modification.
# Regarding groups and permissions:
    # - If the user's account_type is "admin", they will see information about the groups they belong to (groups_info)
# as well as all the permissions they have, whether from groups or user_permissions.
    # - If it's a personal account (regular user), they will be left blank [] to indicate that they do not have administrative permissions.
# Regarding updates:
    # - Users can change their basic information (such as name, phone number, email, and avatar).
    # - If the avatar is new, we use `handle_file_update` to keep the old files organized.
    # - Sensitive fields are never changed (is_staff, is_active, groups, etc.).
# The purpose of this Serializer is:
    # - To enable any user to view and edit their profile securely.
    # - To protect permissions and sensitive fields from any unauthorized modification.
# =====================================================================================================================
class ProfileSerializer(serializers.ModelSerializer):
    groups_info = serializers.SerializerMethodField(read_only=True)
    permissions = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'phone',
            'first_name', 'last_name', 'avatar',
            'account_type', 'is_active', 'is_staff',
            'groups_info', 'permissions', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'account_type', 'is_staff', 'created_at', 'updated_at', 'permissions', 'groups', 'is_active']
    
    def get_groups_info(self, object):
        if object.account_type != 'admin':
            return [] 
        
        return [
            {'id': group.id,  'name': group.name}
            for group in object.groups.all()
        ]
    
    def get_permissions(self, object):
        if object.account_type != 'admin':
            return []         
        user_permissions = []
        for group in object.groups.all():
            for permission in group.permissions.all():
                full_perm = f"{permission.content_type.app_label}.{permission.codename}"
                user_permissions.append(full_perm)
        
        for permission in object.user_permissions.all():
            full_perm = f"{permission.content_type.app_label}.{permission.codename}"
            user_permissions.append(full_perm)
        
        return list(set(user_permissions))
    
    def update(self, instance, validated_data):
        if "avatar" in validated_data:
            handle_file_update(validated_data.get("avatar"), instance.avatar)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance
# =====================================================================================================================




