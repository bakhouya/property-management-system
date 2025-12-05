
import uuid
from django.db import models


# ============================================================================================
# A Model representing the category type, such as Sale or Rent.
# This Model is used to store the basic data for each category type,
# making it easier to manage different category types within the application.
# ============================================================================================
class CategoryType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True, default="")
   
    image = models.ImageField(upload_to="categories/type/", blank=True, null=True)
    status = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Category Type"
        verbose_name_plural = "Categories Types"
        ordering = ['-created_at']  


    def __str__(self):
        return f"{self.title} ({'Active' if self.status else 'Inactive'})"
    
    def toggle_status(self):
        self.status = not self.status
        self.save()
        return self
# ============================================================================================
# End CategoryType    
# ============================================================================================
# 
# 
# 
# 
# 
# ============================================================================================
# A model representing the main categories within the system.
# Used to classify basic elements such as residential or commercial units.
# This model allows for hierarchical data organization 
# ============================================================================================
class MainCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True, default="")
   
    image = models.ImageField(upload_to="categories/main/", blank=True, null=True)
    status = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Main Category"
        verbose_name_plural = "Main Categories"
        ordering = ['-created_at']  


    def __str__(self):
        return f"{self.title} ({'Active' if self.status else 'Inactive'})"
    
    def toggle_status(self):
        self.status = not self.status
        self.save()
        return self
    
# ============================================================================================
# End MainCategory    
# ============================================================================================
# 
# 
# 
# 
# 
# ============================================================================================
# A model representing subcategories linked to main categories.
# For example: apartments, villas, land subdivisions, etc.
# This model inherits the relationship from the MainCategory model to link each subcategory to the appropriate main category.
# It also connects to the CategoryType model to more precisely define the category type.
# ============================================================================================
class SubCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True, default="")
    image = models.ImageField(upload_to="categories/sub/", blank=True, null=True)
    status = models.BooleanField(default=True) 
    # main parent field: used from model "MainCategory"    
    main = models.ForeignKey(MainCategory, on_delete=models.CASCADE, related_name="sub_categories")
    # types relationship with model "CategoryType" 
    types = models.ManyToManyField(CategoryType, related_name="subcategories")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Sub Category"
        verbose_name_plural = "Sub Categories"
        ordering = ['-created_at']  


    def __str__(self):
        return f"{self.title} ({'Active' if self.status else 'Inactive'})"

    def toggle_status(self):
        self.status = not self.status
        self.save()
        return self
# ============================================================================================
# End SubCtaegory    
# ============================================================================================
