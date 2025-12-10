
# ====================================================================================================
# ====================================================================================================
from django.forms import ValidationError
from rest_framework import serializers

from categories.rules import CATEGORY_TYPE_RULES, MAIN_CATEGORY_RULES, SUB_CATEGORY_RULES
from utils.helpers import handle_file_update
from utils.validators import DynamicValidator
from .models import CategoryType, MainCategory, SubCategory
# ====================================================================================================


# ====================================================================================================
# serializer CategoryTypeSerializer: to get items list, create, update, delete 
# ====================================================================================================
class CategoryTypeSerializer(serializers.ModelSerializer): 
    sub_categories_count = serializers.SerializerMethodField() 
    properties_count = serializers.SerializerMethodField() 

    class Meta:
        model = CategoryType
        fields = "__all__"
        read_only_fields = ['id', 'created_at', 'updated_at', 'sub_categories_count', 'properties_count'] 

    # ========================================================================
    # get subcategories count to list
    def get_sub_categories_count(self, categoryTypeObject):
        return categoryTypeObject.subcategories.count()
    # ========================================================================
    
    # ========================================================================
    # get properties count to list 
    def get_properties_count(self, categoryTypeObject):
        return categoryTypeObject.properties.count()   
    
    # ========================================================================
    # dynamic validator with costom rules 
    def to_internal_value(self, data):
        is_update = self.instance is not None
        validator = DynamicValidator(CategoryType, instance=self.instance if is_update else None)        
        try:
            validation_data = validator.validate(data, CATEGORY_TYPE_RULES, is_update=is_update)
        except ValidationError as error:
            raise serializers.ValidationError(error.message_dict)
        return super().to_internal_value(validation_data)
    # ========================================================================

    # ========================================================================
    # when user admin change image : delete old image in folder static
    def update(self, instance, data):
        if "image" in data:
            handle_file_update(data.get("image"), instance.image)
        
        for attr, value in data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance
    # ========================================================================
# ====================================================================================================
# 
# ====================================================================================================
# serializer MainCategorySerializer: to get items list, create, update, delete 
# ====================================================================================================
class MainCategorySerializer(serializers.ModelSerializer):
    sub_categories_count = serializers.SerializerMethodField()  
    properties_count = serializers.SerializerMethodField()   

    class Meta:
        model = MainCategory
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'sub_categories_count', 'properties_count']

    # ========================================================================
    # get count sub_categorries from relationship ManyToMany
    # sub_categories is name related_name in model 
    def get_sub_categories_count(self, categoryTypeObject):
        return categoryTypeObject.sub_categories.count()
    # ========================================================================

    # ========================================================================
    # get properties count
    def get_properties_count(self, categoryTypeObject):
        return categoryTypeObject.properties.count()
    
    # ========================================================================
    # dynamic validator with costom rules 
    def to_internal_value(self, data):
        validator = DynamicValidator(MainCategory, instance=None)
        is_update = self.instance is not None         
        try:
            cleaned_data = validator.validate(data, MAIN_CATEGORY_RULES, is_update=is_update)
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)
        return super().to_internal_value(cleaned_data)
    # ========================================================================

    # ========================================================================
    # if user admin change image file : delete ild image in dir static
    def update(self, instance, data):
        if "image" in data:
            handle_file_update(data.get("image"), instance.image)        
        for attr, value in data.items():
            setattr(instance, attr, value)        
        instance.save()
        return instance
    # ========================================================================
# ====================================================================================================
# 
# ====================================================================================================
# serializer MainCategorySerializer: to get items list, create, update, delete, get item
# ====================================================================================================
class SubCategorySerializer(serializers.ModelSerializer):
    main = MainCategorySerializer(read_only=True)
    types = CategoryTypeSerializer(many=True, read_only=True)
    main_id = serializers.PrimaryKeyRelatedField(queryset=MainCategory.objects.all(), source='main',  write_only=True)
    type_ids = serializers.PrimaryKeyRelatedField(queryset=CategoryType.objects.all(), source='types', many=True, write_only=True)
    properties_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = SubCategory
        fields = fields = ['id', 'title', 'description', 'image','status',
            'main',          
            'main_id',       
            'types',          
            'type_ids',       
            'properties_count',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    # ========================================================================
    # dynamic validator with costom rules 
    def to_internal_value(self, data):
        is_update = self.instance is not None
        validator = DynamicValidator(SubCategory, instance=self.instance if is_update else None)        
        try:
            validation_data = validator.validate(data, SUB_CATEGORY_RULES, is_update=is_update)
        except ValidationError as error:
            raise serializers.ValidationError(error.message_dict)
        return super().to_internal_value(validation_data)
    # ========================================================================
    # ========================================================================
    def get_properties_count(self, object):
        return object.properties.count()
    # ========================================================================
    # ========================================================================
    # handle create item
    def create(self, data):
        if 'types' in data:
            types_data = data.pop('types')
        sub_category = SubCategory.objects.create(**data)
        if types_data: 
            sub_category.types.set(types_data)
        return sub_category
    
    # ========================================================================
    # update item data with types if has     
    def update(self, instance, data):
        # delete old image if change image
        if "image" in data:
            handle_file_update(data.get("image"), instance.image) 

        types_data = data.pop('types', None)  

        for attr, value in data.items():
            setattr(instance, attr, value)        
        instance.save() 

        if types_data is not None:
            instance.types.set(types_data)
        
        return instance
# ====================================================================================================
# 
# ====================================================================================================
# serializer BasicSubCategorySerializer: get item : call in MainCategoryWithSubsSerializer, CategoryTypeWithSubsSerializer
# ====================================================================================================
class BasicSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'
        read_only_fields = ['id', 'created_at']
# ====================================================================================================
# 
# ====================================================================================================
# serializer MainCategoryWithSubsSerializer:  get item
# ====================================================================================================
class MainCategoryWithSubsSerializer(serializers.ModelSerializer):
    sub_categories = BasicSubCategorySerializer(many=True, read_only=True)    
    class Meta:
        model = MainCategory
        fields = '__all__'
# ====================================================================================================
# 
# ====================================================================================================
# serializer CategoryTypeWithSubsSerializer:  get item
# ====================================================================================================
class CategoryTypeWithSubsSerializer(serializers.ModelSerializer):
    sub_categories = BasicSubCategorySerializer(many=True, read_only=True, source='subcategories')    
    class Meta:
        model = CategoryType
        fields = '__all__'
# ====================================================================================================

