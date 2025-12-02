

import uuid
from django.db import models
from django.conf import settings

# ============================================================================================
# PlatformSettings Model:
# This form is used to store basic platform settings such as title, description, logos, icons
# It should contain only one record in the database.
# ============================================================================================
class PlatformSettings(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    dark_logo = models.ImageField(upload_to="settings/platform/", blank=True, null=True, verbose_name="Dark Logo")
    light_logo = models.ImageField(upload_to="settings/platform/", blank=True, null=True, verbose_name="Light Logo")
    favicon = models.ImageField(upload_to="settings/platform/", blank=True, null=True)
    
    contact_email = models.EmailField(blank=True, null=True, verbose_name="Contact Email")
    support_email = models.EmailField(blank=True, null=True, verbose_name="Support Email")
    phone = models.CharField(max_length=20, blank=True, null=True)
    
    timezone = models.CharField(max_length=100, default='Africa/Casablanca')
    currency = models.CharField(max_length=10, default='MAD')
    currency_symbol = models.CharField(max_length=10, default='dh', verbose_name="Currency Symbol")

    maintenance_mode = models.BooleanField(default=False, verbose_name="Maintenance Mode")
    allow_registration = models.BooleanField(default=True, verbose_name="Allow User Registration")
   
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Platform Settings"
        verbose_name_plural = "Platform Settings"

    def __str__(self):
        return f"{self.title} - Settings"
    
    # ======================================================================================
    # This function ensures that only one record is saved in the database.
    # If there are pre-existing settings, it prevents the creation of a new record 
    # updates the existing record instead of adding a new one.
    # ======================================================================================
    def save(self, *args, **kwargs):
        if PlatformSettings.objects.exists() and not self.pk:
            settings = PlatformSettings.objects.first()
            self.id = settings.id
            self.pk = settings.pk
        super().save(*args, **kwargs)
    # ======================================================================================

    # ======================================================================================
    # This function returns the existing platform settings,
    # and if none exist, it automatically creates a new record with default settings.
    # ======================================================================================
    @classmethod
    def get_settings(cls):
        if cls.objects.exists():
            return cls.objects.first()
        else:
            return cls.objects.create(
                title='Real Estate Platform',
                description='A platform for buying and renting real estate in Morocco.',
                currency='MAD',
                currency_symbol='DH',
                timezone='Africa/Casablanca',
                contact_email='kamfour1997@gmail.com',
                support_email='kamfour1997@gmail.com',
                phone='0772013984'
            )
    # ====================================================================================== 
# ============================================================================================
# End Platform Settings Model
# ============================================================================================
# 
#
# 
#  
# ============================================================================================
# This is a social media data model, containing only one database item.
# It stores social media links (such as Facebook, Instagram, etc.) independently, 
# and when the data is retrieved, it is returned as an array, displaying only the active links.
# ============================================================================================
class SocialMediaSettings(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    facebook    = models.URLField(blank=True, null=True, verbose_name="Facebook URL")
    whatsapp    = models.URLField(blank=True, null=True, verbose_name="WhatsApp URL")
    twitter     = models.URLField(blank=True, null=True, verbose_name="Twitter URL")
    instagram   = models.URLField(blank=True, null=True, verbose_name="Instagram URL")
    linkedin    = models.URLField(blank=True, null=True, verbose_name="LinkedIn URL")
    tiktok      = models.URLField(blank=True, null=True, verbose_name="TikTok URL")
    telegram    = models.URLField(blank=True, null=True, verbose_name="Telegram URL")
    youtube     = models.URLField(blank=True, null=True, verbose_name="YouTube URL")

    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Updated")

    class Meta:
        verbose_name = "Social Media Settings"
        verbose_name_plural = "Social Media Settings"

    def __str__(self):
        return "Social Media Settings"

    # ======================================================================================
    # method to ensure only one instance exists
    # ======================================================================================
    def save(self, *args, **kwargs):
        if SocialMediaSettings.objects.exists() and not self.pk:
            existing = SocialMediaSettings.objects.first()
            self.id = existing.id
            self.pk = existing.pk
        super().save(*args, **kwargs)

    # ======================================================================================
    # method to create or get default social media settings
    # ======================================================================================
    @classmethod
    def get_social_media_settings(cls):
        if cls.objects.exists():
            return cls.objects.first()
        else:
            return cls.objects.create(
                facebook ="https://facebook.com/yourpage",
                instagram ="https://instagram.com/yourprofile",
                twitter ="https://twitter.com/yourprofile",
                linkedin ="https://linkedin.com/yourprofile",
                whatsapp ="https://wa.me/212772013984",
                tiktok ="https://tiktok.com/yourprofile",
                telegram ="https://telegram.com/yourprofile",
                youtube ="https://youtube.com/yourprofile",
            )
    # ======================================================================================

    # ======================================================================================
    # utility methods
    # ======================================================================================
    def get_active_social_media(self):
        social_media = []
        platforms = [
            ('facebook', 'Facebook', self.facebook),
            ('whatsapp', 'WhatsApp', self.whatsapp),
            ('twitter', 'Twitter', self.twitter),
            ('instagram', 'Instagram', self.instagram),
            ('linkedin', 'LinkedIn', self.linkedin),
            ('tiktok', 'TikTok', self.tiktok),
            ('telegram', 'Telegram', self.telegram),
            ('youtube', 'YouTube', self.youtube)
        ]
        
        for platform_id, platform_name, url in platforms:
            if url:
                social_media.append({
                    'id': platform_id,
                    'name': platform_name,
                    'url': url,
                    'icon_class': f'fab fa-{platform_id}'
                })
        
        return social_media
# ============================================================================================
# End Social Media Settings
# ============================================================================================
# 
#
# 
#  
# ============================================================================================
# A model representing Moroccan cities that allows managing the activation status of each city.
# It contains the following functions:
# 1. get_active_cities(): Returns a list of only the active cities.
# 2. toggle_status(): Changes the activation status of a city from active to inactive or vice versa.
# ============================================================================================
class City(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    status = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"
        ordering = ['name']  

    def __str__(self):
        return f"{self.name} ({'Active' if self.status else 'Inactive'})"

    # ======================================================================================
    # Methods utilitaires
    # ======================================================================================
    @classmethod
    def get_active_cities(cls):
        return cls.objects.filter(status=True).order_by('name')
    
    def toggle_status(self):
        self.status = not self.status
        self.save()
        return self.status
# ============================================================================================
# End Cities
# ============================================================================================
# 
#
# 
# 
# ============================================================================================
# A dedicated form for storing basic search engine optimization (SEO) settings.
# Used to save general information such as the title, description, keywords,
# This form helps in easily managing the website's SEO settings and improving the platform's ranking in search results.
# ============================================================================================
class SeoSettings(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, default="My Platform")
    description = models.TextField(blank=True, null=True)
    keywords = models.TextField(blank=True, null=True)

    google_analytics_id = models.CharField(max_length=100, blank=True, null=True)
    facebook_pixel_id = models.CharField(max_length=100, blank=True, null=True)
    tiktok_pixel_id = models.CharField(max_length=100, blank=True, null=True)
    
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "SEO Settings"
        verbose_name_plural = "SEO Settings"

    def __str__(self):
        return "SEO Settings"

    # ======================================================================================
    # method to ensure only one instance exists
    # ======================================================================================
    def save(self, *args, **kwargs):
        if SeoSettings.objects.exists() and not self.pk:
            existing = SeoSettings.objects.first()
            self.id = existing.id
            self.pk = existing.pk
        super().save(*args, **kwargs)

    # ======================================================================================
    # method to create or get default SEO settings
    # ======================================================================================
    @classmethod
    def get_seo_settings(cls):
        if cls.objects.exists():
            return cls.objects.first()
        else:
            return cls.objects.create(
                title="Real Estate Platform",
                description="A platform for buying and renting real estate in Morocco.",
                keywords="real estate, property, morocco, buy, rent, casa, rabat",
            )
    # ======================================================================================
# ============================================================================================
# End Seo Settings 
# ============================================================================================
# 
#
# 
# 
# ============================================================================================
# A dedicated form for storing the system's core security settings.
# Used to define CORS settings and grant permissions to trusted domains
# that are allowed to access the platform's APIs.
# This form helps strengthen platform security and prevent unauthorized requests from external sources.
# ============================================================================================
class SecuritySettings(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    enable_cors = models.BooleanField(default=True)
    allowed_cors = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Security Settings"
        verbose_name_plural = "Security Settings"

    def __str__(self):
        return "Security Settings"

    # ======================================================================================
    # method to ensure only one instance exists
    # ======================================================================================
    def save(self, *args, **kwargs):
        if SecuritySettings.objects.exists() and not self.pk:
            existing = SecuritySettings.objects.first()
            self.id = existing.id
            self.pk = existing.pk
        super().save(*args, **kwargs)
    # ======================================================================================
    # method to create or get default security settings
    # ======================================================================================
    @classmethod
    def get_security_settings(cls):
        if cls.objects.exists():
            return cls.objects.first()
        else:
            return cls.objects.create(
                enable_cors=True,
                allowed_cors="http://localhost:8000, http://127.0.0.1:8000",
            )
    # ======================================================================================

    def get_allowed_cors_list(self):
        if self.allowed_cors:
            return [origin.strip() for origin in self.allowed_cors.split(',') if origin.strip()]
        return []
    
# ============================================================================================
# End Security Settings
# ============================================================================================
# 
#
# 
# 
# ============================================================================================
# A customizable model for storing each user's personal settings.
# Allows each user to control a set of simple settings specific to their account within the platform.
# The relationship is based on a one-to-one system, meaning each user has only one setting, 
# ensuring that settings are customized independently for each user without duplication.
# ============================================================================================
class UserSettings(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='settings', verbose_name="User")

    contact_whatsapp = models.BooleanField(default=True, )
    number_whatsapp = models.CharField(max_length=20, blank=True, null=True, verbose_name="WhatsApp Number")

    contact_vocal = models.BooleanField(default=True)
    number_vocal = models.CharField(max_length=20, blank=True, null=True, verbose_name="Call Number")

    contact_email = models.BooleanField(default=True)  

    show_profile = models.BooleanField(default=True, verbose_name="Show Profile Publicly")
    show_contact_info = models.BooleanField(default=True, verbose_name="Show Contact Information")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "User Settings"
        verbose_name_plural = "Users Settings"
        ordering = ['-created_at']

    def __str__(self):
        return f"Settings for {self.user.username}"
# ============================================================================================
# End User Settings
# ============================================================================================
