from django.contrib import admin
from .models import CategoryType, MainCategory, SubCategory



# ========================================================================
# Register CategoryType, MainCategory, SubCategory Models
# ========================================================================
admin.site.register(CategoryType)
admin.site.register(MainCategory)
admin.site.register(SubCategory)
# ========================================================================
