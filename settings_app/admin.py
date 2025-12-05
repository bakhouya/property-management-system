from django.contrib import admin
from .models import PlatformSettings, SocialMediaSettings, City, SeoSettings, SecuritySettings, UserSettings

# ========================================================
#  register Settings Models
# ========================================================
admin.site.register(PlatformSettings)
admin.site.register(SocialMediaSettings)
admin.site.register(City)
admin.site.register(SeoSettings)
admin.site.register(SecuritySettings)
admin.site.register(UserSettings)
# ========================================================
