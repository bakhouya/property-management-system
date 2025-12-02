from django.contrib import admin
from .models import PriceType, Property, PropertyImage, Comment

# ========================================================
#  register PriceType, Property, PropertyImage, Comment, Models
# ========================================================
admin.site.register(PriceType)
admin.site.register(Property)
admin.site.register(PropertyImage)
admin.site.register(Comment)
# ========================================================
