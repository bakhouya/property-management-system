
# ============================================================================================
from django.contrib.auth.models import Group, Permission
from django.forms import ValidationError
from rest_framework import serializers
from roles.rules import GROUP_RULES
from utils.validators import DynamicValidator
# ============================================================================================








# ============================================================================================
# Permission serializers
# ============================================================================================
class PermissionSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Permission
        fields = ['id', 'codename', 'name']
# ============================================================================================
# 
# 
# 
# 
# ============================================================================================
# Group serializers
# ============================================================================================
class GroupSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)
    permissions_count = serializers.IntegerField(source='permissions.count', read_only=True)
    users_count = serializers.IntegerField(source='user_set.count', read_only=True)

    permission_ids = serializers.PrimaryKeyRelatedField(
        queryset=Permission.objects.all(),
        many=True,
        write_only=True,
        required=False,
        source='permissions'  
    )
    
    class Meta:
        model = Group
        fields = [
            'id', 'name', 
            'permissions',           
            'permissions_count',    
            'users_count',          
            'permission_ids'        
        ]
    
    # ================================================================
    # call Daynamic validation
    # ================================================================
    def to_internal_value(self, data):
        validator = DynamicValidator(Group, instance=self.instance)
        is_update = self.instance is not None
        try:
            cleaned_data = validator.validate(data, GROUP_RULES, is_update=is_update)
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)

        return super().to_internal_value(cleaned_data)
    # ================================================================
    
    # ================================================================
    # Create group with permissions
    # ================================================================
    def create(self, validated_data):
        permissions = validated_data.pop('permissions', [])
        group = Group.objects.create(**validated_data)
        
        if permissions:
            group.permissions.set(permissions)
        
        return group
    # ================================================================

    # ================================================================
    # Update group with permissions
    # ================================================================
    def update(self, instance, validated_data):
        permissions = validated_data.pop('permissions', None)
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        if permissions is not None:
            instance.permissions.set(permissions)
        
        return instance
    # ================================================================
# ============================================================================================
   
    