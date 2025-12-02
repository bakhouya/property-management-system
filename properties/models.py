
import uuid
from django.db import models
from django.conf import settings
from categories.models import CategoryType, MainCategory, SubCategory
from settings_app.models import City
from visitors.models import Visitor

# ==========================================================================================================
# A dedicated form for defining the types of pricing options available on the platform,
# such as monthly, daily, annual, fixed, or negotiable prices.
# This form aims to organize the different pricing methods and link them to the properties listed,
# thus helping to clearly and systematically determine the appropriate price for each property.
# ==========================================================================================================
class PriceType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True, verbose_name="Name")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    status = models.BooleanField(default=True, verbose_name="Status")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Price Type"
        verbose_name_plural = "Price Types"
        ordering = ['name']

    def __str__(self):
        return self.name

    # ======================================================================================
    # A function designed to return all objects with an active status (status = True).
    # We need to call it within views.py when creating a new property,
    # to select the price type from among the active types only.
    # The function works at the class level, and therefore it is defined as @classmethod.
    # ======================================================================================  
    @classmethod
    def active_price_types(modelClass):
        return modelClass.objects.filter(status=True)
    # ======================================================================================
    # 
    # 
    # 
    # ======================================================================================
    # A function dedicated to creating default items within this model.
    # It is executed only when called at any point within the project.
    # It will be called within the apps.py file inside the ready() function to run once when the application starts,
    # to ensure that default types are created in the database if they do not already exist.
    # ====================================================================================== 
    @classmethod
    def default_types(modelClass):
        if not modelClass.objects.exists():
            default_types = [
                {'name': 'fixed_sale', 'description': 'Fixed Sale Price'},
                {'name': 'negotiable_sale', 'description': 'Negotiable Sale Price'},
                {'name': 'auction', 'description': 'Auction'},
                {'name': 'monthly_rent', 'description': 'Monthly Rent'},
                {'name': 'daily_rent', 'description': 'Daily Rent'},
                {'name': 'yearly_rent', 'description': 'Yearly Rent'},
                {'name': 'negotiable_rent', 'description': 'Negotiable Rent'},
                {'name': 'seasonal_rent', 'description': 'Seasonal Rent'},
                {'name': 'vacation_rent', 'description': 'Vacation Rent'},
            ]
            
            for type_data in default_types:
                modelClass.objects.create(**type_data)
            
            return True
        return False
    # ======================================================================================  
# ==========================================================================================================
# End PriceType Model
# ==========================================================================================================
# 
# 
# 
# 
# ==========================================================================================================
# A dedicated form for storing essential property data within the platform.
# This form includes detailed property information such as address, area, classification type, city ...
# It also contains fields for tracking property status, activation or blocking, and the number of visits and likes, 
# # providing a comprehensive structure for managing and showcasing properties to users in a professional manner.
# ==========================================================================================================
class Property(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, verbose_name="Property Title")
    description = models.TextField(blank=True, null=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='properties')
    category_type = models.ForeignKey(CategoryType, on_delete=models.SET_NULL, null=True, blank=True, related_name='properties', verbose_name="Category Type")
    main_category = models.ForeignKey(MainCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='properties', verbose_name="Main Category")
    sub_category = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='properties', verbose_name="Sub Category")
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True, related_name='properties', verbose_name="City")
    
    address = models.TextField(blank=True, null=True, verbose_name="Full Address")
    area = models.DecimalField(max_digits=10, decimal_places=2)
    is_owner = models.BooleanField(default=True, verbose_name="Is Owner")

    price = models.DecimalField(max_digits=15, decimal_places=2,  verbose_name="Price")   
    price_type = models.ForeignKey(PriceType, on_delete=models.SET_NULL, null=True, blank=True, related_name='properties', verbose_name="Price Type")
    video = models.FileField(upload_to="properties/videos/", blank=True, null=True, verbose_name="Property Video")

    status = models.BooleanField(default=True)   
    is_blocked = models.BooleanField(default=False, verbose_name="Is Blocked")

    # Relationships are designed to track visitor and user interaction with the property (visits, likes, favorites).
    # ManyToMany was used because both parties can have multiple interactions.
    # Symmetrical was set to False because the relationship is unidirectional:
    # The user or visitor interacts with the property, not the other way around.
    views = models.ManyToManyField(Visitor, blank=True, symmetrical=False, related_name='property_views')   
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, symmetrical=False, related_name='property_likes')   
    favorites = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, symmetrical=False, related_name='property_favorites')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Property"
        verbose_name_plural = "Properties"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'is_blocked']),
            models.Index(fields=['city', 'price']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        user_name = getattr(self.user, "username", None) or getattr(self.user, "phone", "Unknown User")
        return f"{self.title} - {user_name}"
    
    # ===============================================================================================================
    # A function designed to retrieve all elements with the active status (status = True).
    # This function is executed when called in views.py to obtain a list of only the active elements.
    # The function operates at the class level, not on a single object.
    # Therefore, it is defined as `@classmethod` so that it processes all records within the database.
    # ===============================================================================================================
    @classmethod
    def active_objects(modelClass):
        return modelClass.objects.filter(status=True)
    # ===============================================================================================================
    # 
    # 
    # ===============================================================================================================
    # A function dedicated to changing the overall status of a property between enabled and disabled.
    # It is called from views.py when you want to enable or disable a specific element
    # This function applies to only one element (instance), and therefore it is not defined as @classmethod.
    # ===============================================================================================================
    def change_status(self):
        self.status = not self.status
        self.save()
        return self
    # ===============================================================================================================
    # 
    # 
    # ===============================================================================================================
    # A function designed to change the blocking state (is_blocked) of a property from True to False
    # or from False to True.
    # This function is executed when called from views.py to block or unblock a property.
    # The function operates on only one instance, therefore it is not defined as @classmethod.
    # ===============================================================================================================
    def change_blocked(self):
        self.is_blocked = not self.is_blocked
        self.save()
        return self
    # ===============================================================================================================

# ==========================================================================================================
# End Property Model
# ==========================================================================================================
# 
# 
# 
# 
# ==========================================================================================================
# # A function dedicated to saving property images within a special folder based on the property ID,
# which ensures that the images are arranged and organized within a clear and separate file structure for each property.
# ==========================================================================================================
def property_image_upload_path(instance, filename):
    import os
    ext = os.path.splitext(filename)[1]  
    unique_filename = f"{uuid.uuid4()}{ext}"
    property_id = instance.property.id if instance.property else "unknown"
    return f"properties/images/{property_id}/{unique_filename}"
# ==========================================================================================================
# A dedicated property image storage model, allowing each property to have multiple images.
# This model aims to separate image management from the property image management model, providing greater flexibility
# in adding an unlimited number of images per property.
# ==========================================================================================================
class PropertyImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)    
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')    
    image = models.ImageField(upload_to=property_image_upload_path, verbose_name="Property Image")
       
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Property Image"
        verbose_name_plural = "Property Images"
        ordering = ['created_at']

    def __str__(self):
        return f"Image for {self.property.title}"
# ==========================================================================================================
# End PropertyImage Model
# ==========================================================================================================   
# 
# 
# 
# 
# ==========================================================================================================
# A dedicated form for managing property-related comments, where users can add comments
# on any property, and they can also reply to other users' comments.
# This form enables the creation of a threaded discussion system that supports main comments and sub-replies,
# helping to enhance interaction within the platform.
# ==========================================================================================================
class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='property_comments')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='comments', verbose_name="Property")
    comment = models.TextField(verbose_name="Comment")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ['-created_at'] 
        indexes = [
            models.Index(fields=['property', 'parent']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        user_name = getattr(self.user, "username", None) or getattr(self.user, "phone", "Unknown User")
        return f"Comment by {user_name} on {self.property.title}"

    # ======================================================================================
    # A function dedicated to switching the suspension state between enabled and disabled,
    # where it flips the current value (True ↔ False) and saves the change in the database.
    # ======================================================================================
    def toggle_status(self):
        self.status = not self.status
        self.save()
        return self.status
# ==========================================================================================================
# End Comment Model
# ==========================================================================================================

