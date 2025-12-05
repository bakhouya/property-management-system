from django.db.models.signals import post_migrate
from django.dispatch import receiver

@receiver(post_migrate)
def create_default_settings(sender, **kwargs):
    if sender.name == 'properties':
        from .models import PriceType
        PriceType.default_types()

