from django.db.models.signals import post_migrate
from django.dispatch import receiver

@receiver(post_migrate)
def create_default_settings(sender, **kwargs):
    if sender.name == 'settings_app':
        from .models import (
            PlatformSettings,
            SocialMediaSettings,
            SeoSettings,
            SecuritySettings
        )
        PlatformSettings.get_settings()
        SocialMediaSettings.get_social_media_settings()
        SeoSettings.get_seo_settings()
        SecuritySettings.get_security_settings()
