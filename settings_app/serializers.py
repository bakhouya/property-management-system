# ============================================================================================
# ============================================================================================
from django.forms import ValidationError
from rest_framework import serializers

from settings_app.rules import CITY_RULES, MEDIA_RULES, PLATFORM_RULES, SECURITY_RULES, SEO_RULES, USER_SETTINGS_RULES
from utils.helpers import handle_file_update
from utils.validators import DynamicValidator
from .models import (PlatformSettings, SocialMediaSettings, City, SeoSettings, SecuritySettings, UserSettings)
from django.contrib.auth import get_user_model
User = get_user_model()




# ============================================================================================
# Platform Settings Serializer
# Responsible for verifying and processing logo and icon files
# ============================================================================================
class PlatformSettingsSerializer(serializers.ModelSerializer):
    # dark_logo = serializers.SerializerMethodField()
    # light_logo = serializers.SerializerMethodField()
    # favicon = serializers.SerializerMethodField()

    class Meta:
        model = PlatformSettings
        fields = '__all__'
        read_only_fields = ['id', 'updated_at']
    

    def to_internal_value(self, data):
        validator = DynamicValidator(PlatformSettings, instance=self.instance)
        is_update = self.instance is not None
        try:
            cleaned_data = validator.validate(data, PLATFORM_RULES, is_update=is_update)
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)

        return super().to_internal_value(cleaned_data)

    def update(self, instance, validated_data):
        if "dark_logo" in validated_data:
            handle_file_update(validated_data.get("dark_logo"), instance.dark_logo) 
        if "light_logo" in validated_data:
            handle_file_update(validated_data.get("light_logo"), instance.light_logo)
        if "favicon" in validated_data:
            handle_file_update(validated_data.get("favicon"), instance.favicon) 
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance
# ============================================================================================
# 
# 
# 
# 
# ============================================================================================
# Social Media Settings Serializer
# Relies on dynamic verification to evaluate submitted data
# ============================================================================================
class SocialMediaSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaSettings
        fields = '__all__'
        read_only_fields = ['id', 'updated_at']
    
    def to_internal_value(self, data):
        validator = DynamicValidator(SocialMediaSettings, instance=self.instance)
        is_update = self.instance is not None
        try:
            cleaned_data = validator.validate(data, MEDIA_RULES, is_update=is_update)
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)

        return super().to_internal_value(cleaned_data)
# ============================================================================================
# 
# 
# 
# 
# ============================================================================================
# SEO Settings Serializer
# Responsible for verifying SEO-related data
# ============================================================================================
class SeoSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeoSettings
        fields = '__all__'
        read_only_fields = ['id', 'updated_at']
    
    def to_internal_value(self, data):
        validator = DynamicValidator(SeoSettings, instance=self.instance)
        is_update = self.instance is not None
        try:
            cleaned_data = validator.validate(data, SEO_RULES, is_update=is_update)
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)

        return super().to_internal_value(cleaned_data)
# ============================================================================================
# 
# 
# 
# 
# ============================================================================================
# Security Settings Serializer
# Checks the security rules specified for updating system settings
# ============================================================================================
class SecuritySettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecuritySettings
        fields = '__all__'
        read_only_fields = ['id', 'updated_at']
    
    def to_internal_value(self, data):
        validator = DynamicValidator(SecuritySettings, instance=self.instance)
        is_update = self.instance is not None
        try:
            cleaned_data = validator.validate(data, SECURITY_RULES, is_update=is_update)
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)

        return super().to_internal_value(cleaned_data)
# ============================================================================================
# 
# 
# 
# 
# ============================================================================================
# City Serializer
# Uses special rules to verify city data before storing it
# ============================================================================================
class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'
        read_only_fields = ['id', 'updated_at']
    
    def to_internal_value(self, data):
        validator = DynamicValidator(City, instance=self.instance)
        is_update = self.instance is not None
        try:
            cleaned_data = validator.validate(data, CITY_RULES, is_update=is_update)
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)

        return super().to_internal_value(cleaned_data)
# ============================================================================================
# 
# 
# 
# 
# ============================================================================================
# User Settings Serializer
# Responsible for verifying the user's communication and visibility settings
# ============================================================================================
class UserSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSettings
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
        
    def to_internal_value(self, data):
        validator = DynamicValidator(UserSettings, instance=self.instance)
        is_update = self.instance is not None
        try:
            cleaned_data = validator.validate(data, USER_SETTINGS_RULES, is_update=is_update)
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)

        return super().to_internal_value(cleaned_data)
# ============================================================================================
# 
# 
# 
# 
# ============================================================================================
# User Settings With User Information Serializer
# Used by the administrator to display any user's settings along with their account information
# ============================================================================================
class UserSettingsWithUserSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(source='user.id', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = UserSettings
        fields = [
            'id', 'user_id', 'username', 'email',
            'contact_whatsapp', 'number_whatsapp',
            'contact_vocal', 'number_vocal',
            'contact_email',
            'show_profile', 'show_contact_info',
            'created_at', 'updated_at'
        ]
        read_only_fields = fields
# ============================================================================================
