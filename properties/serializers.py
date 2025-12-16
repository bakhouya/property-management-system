
from rest_framework import serializers
from django.core.exceptions import ValidationError
from properties.rules import COMMENT_RULES, PRICETYPE_RULES, PROPERTY_RULES
from utils.helpers import handle_file_update
from utils.validators import DynamicValidator
from .models import PriceType, Property, PropertyImage, Comment
from categories.models import CategoryType, MainCategory, SubCategory
from settings_app.models import City
from categories.models import CategoryType, MainCategory, SubCategory

from django.contrib.auth import get_user_model
User = get_user_model()



# =============================================================================================================================
# 
# =============================================================================================================================
# Simple Serializer for displaying user data
# Used within other serializers (comments, properties, etc.)
# All fields are read-only
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'avatar']
        read_only_fields = fields
# Serializer is used to display the categories type within the real estate app.
# ref_name is used to avoid name conflicts with the categories app.
class CateforyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryType
        ref_name = "PropertiesCategoryType" 
        fields = ['id', 'title']
        read_only_fields = fields
# Serializer to display the main categories
class MainCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MainCategory
        ref_name = "PropertiesMainCategory" 
        fields = ['id', 'title']
        read_only_fields = fields
# Serializer to display the sub categories
class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        ref_name = "PropertiesSubCategory" 
        fields = ['id', 'title']
        read_only_fields = fields
# =============================================================================================================================






# =============================================================================================================================
#  # Serializer is specific to pricing types.
# It relies on DynamicValidator to apply different rules between creation and update.
# =============================================================================================================================
class PriceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceType
        fields = ['id', 'name', 'description', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def to_internal_value(self, data):
        is_update = self.instance is not None
        validator = DynamicValidator(PriceType, instance=self.instance if is_update else None)        
        try:
            validation_data = validator.validate(data, PRICETYPE_RULES, is_update=is_update)
        except ValidationError as error:
            raise serializers.ValidationError(error.message_dict)
        return super().to_internal_value(validation_data) 
# =============================================================================================================================

# 
# =============================================================================================================================
#  Serializer (Property Images)                    
# =============================================================================================================================
class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['id', 'image']
        read_only_fields = ['id']
# =============================================================================================================================
# 
# =============================================================================================================================
# Serializer Comments
# =============================================================================================================================
class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField(read_only=True)   
    class Meta:
        model = Comment
        fields = ['id', 'user', 'property', 'comment', 'parent', 'status', 'replies', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at', 'replies']
     
    #  get dynamic validation rules for create and update
    def to_internal_value(self, data):
        is_update = self.instance is not None
        validator = DynamicValidator(Comment, instance=self.instance if is_update else None)        
        try:
            validation_data = validator.validate(data, COMMENT_RULES, is_update=is_update)
        except ValidationError as error:
            raise serializers.ValidationError(error.message_dict)
        return super().to_internal_value(validation_data)       
   
    # get replies for comment 
    def get_replies(self, object):
        if object.replies.exists():
            serializer = CommentSerializer(object.replies.all(), many=True)
            return serializer.data
        return []
    
    # create comment with user from request
    def create(self, data):
        data['user'] = self.context['request'].user
        return super().create(data)
# =============================================================================================================================
    


# =============================================================================================================================
# Serializer Property deteils                
# =============================================================================================================================
class PropertyDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    city = serializers.StringRelatedField(read_only=True)
    price_type = serializers.StringRelatedField(read_only=True)   
    category_type = CateforyTypeSerializer(read_only=True)
    main_category = MainCategorySerializer(read_only=True)
    sub_category = SubCategorySerializer(read_only=True)
  
    comments = serializers.SerializerMethodField(read_only=True)
    images = PropertyImageSerializer(many=True, read_only=True)

    comments_count = serializers.SerializerMethodField(read_only=True)
    views_count = serializers.SerializerMethodField(read_only=True)
    likes_count = serializers.SerializerMethodField(read_only=True)
    favorites_count = serializers.SerializerMethodField(read_only=True)
    is_liked = serializers.SerializerMethodField(read_only=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Property
        fields = ['id', 'title', 'description', 'user', 'category_type', 'main_category', 'sub_category',
            'city', 'address', 'area', 'is_owner', 'price', 'price_type', 'video', 'status', 'is_blocked',
            'views_count', 'comments_count', 'likes_count', 'favorites_count', 'is_liked', 'is_favorited', 'images', 'comments',
             'created_at', 'updated_at']
        read_only_fields =  fields

    def get_comments(self, object):
        if object.comments.exists():
            serializer = CommentSerializer(object.comments.filter(parent=None), many=True)
            return serializer.data
        return []
    
    def get_comments_count(self, object):
        return object.comments.count()
    
    def get_views_count(self, object):
        return object.views.count()
    
    def get_likes_count(self, object):
        return object.likes.count()
    
    def get_favorites_count(self, object):
        return object.favorites.count()
    
    def get_is_liked(self, object):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return object.likes.filter(id=request.user.id).exists()
        return False
    
    def get_is_favorited(self, object):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return object.favorites.filter(id=request.user.id).exists()
        return False
# =============================================================================================================================
# 
# =============================================================================================================================
# Serializer Property create and update 
# =============================================================================================================================
class PropertyCreateSerializer(serializers.ModelSerializer):

    images = serializers.ListField(child=serializers.ImageField(), write_only=True)   
    category_type = serializers.UUIDField(write_only=True)
    main_category = serializers.UUIDField(write_only=True)
    sub_category = serializers.UUIDField(write_only=True)
    city = serializers.UUIDField(write_only=True)
    price_type = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = Property
        fields = ['title', 'description', 'category_type', 'main_category', 'sub_category', 'city', 'address', 'area',
            'is_owner', 'price', 'price_type', 'video', 'images']
        read_only_fields = ['user']
    
    # ========================================================================
    # dynamic validator with costom rules 
    def to_internal_value(self, data):
        is_update = self.instance is not None
        validator = DynamicValidator(Property, instance=self.instance if is_update else None)        
        try:
            validation_data = validator.validate(data, PROPERTY_RULES, is_update=is_update)
        except ValidationError as error:
            raise serializers.ValidationError(error.message_dict)
        return super().to_internal_value(validation_data)
    # ========================================================================

    def create(self, data):
        if "images" in data:
            images = data.pop('images', [])       
        data['category_type']   = CategoryType.objects.get(id=data.pop('category_type'))
        data['main_category']   = MainCategory.objects.get(id=data.pop('main_category'))
        data['sub_category']    = SubCategory.objects.get(id=data.pop('sub_category'))
        data['city']            = City.objects.get(id=data.pop('city'))
        data['price_type']      = PriceType.objects.get(id=data.pop('price_type'))
        data['user']            = self.context['request'].user

        property_created = super().create(data)
        if property_created:
            for image in images:
                PropertyImage.objects.create(property=property_created, image=image)
        
        return property_created
    
    def update(self, instance, data):
        if 'images' in data:
            images = data.pop('images', [])
        
        if 'category_type' in data:
            instance.category_type = CategoryType.objects.get(id=data.pop('category_type'))       
        if 'main_category' in data:
            instance.main_category = MainCategory.objects.get(id=data.pop('main_category'))       
        if 'sub_category' in data:
            instance.sub_category = SubCategory.objects.get(id=data.pop('sub_category'))        
        if 'city' in data:
            instance.city = City.objects.get(id=data.pop('city'))        
        if 'price_type' in data:
            instance.price_type = PriceType.objects.get(id=data.pop('price_type'))
        
        updated = super().update(instance, data)
        
        if updated:
            if "image" in images:  
                image_file = images["image"]
                handle_file_update(image_file, instance.image)
            
            for key, image_file in images.items():
                if key != "image":  
                    PropertyImage.objects.create(property=updated, image=image_file)
            
        return instance
# =============================================================================================================================
# 
# =============================================================================================================================
# Serializer Property globals 
# =============================================================================================================================
class PropertyListSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    city = serializers.StringRelatedField(read_only=True)
    price_type = serializers.StringRelatedField(read_only=True)
    category_type = CateforyTypeSerializer(read_only=True)
    main_category = MainCategorySerializer(read_only=True)
    sub_category = SubCategorySerializer(read_only=True)
    
    images = PropertyImageSerializer(many=True, read_only=True)
    views_count = serializers.SerializerMethodField(read_only=True)
    likes_count = serializers.SerializerMethodField(read_only=True)
    comments_count = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Property
        fields = ['id', 'title', 'description', 'user', 
                  'city', 'address', 'area', 'category_type', 
                  'price', 'price_type', 'main_category',
                  'sub_category', 'status', 'is_blocked', 
                  'views_count', 'likes_count', 'comments_count', 
                  'images', 'created_at']
        
    
    def get_views_count(self, object):
        return object.views.count()
    
    def get_likes_count(self, object):
        return object.likes.count()
    
    def get_comments_count(self, object):
        return object.comments.count()
# =============================================================================================================================








