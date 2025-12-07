
# ============================================================================================
from django.contrib.auth.models import Group, Permission
from django.forms import ValidationError
from rest_framework import serializers
from roles.rules import GROUP_RULES
from utils.validators import DynamicValidator
# ============================================================================================








# ============================================================================================
# A simple serializer for displaying permissions information, relying only on the basic fields.
# (id, codename, and name) without any additional logic, as the goal is to display the data as is.
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
# This Serializer is responsible for managing group data and its associated permissions.
# The permissions and users associated with each group are displayed, along with their totals.
# The permission_ids field has also been added to facilitate the submission of permissions during creation or updates.
# Additionally, data is passed through a dynamic validator before saving to ensure the accuracy of the input.
# Finally, the creation and update processes have been optimized to ensure that the permissions associated with each group are saved correctly.
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
   
    