from django.apps import AppConfig


class SettingsAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'settings_app'

    def ready(self):
        # =====================================================
        # run create default price types in databse
        # =====================================================
        import settings_app.signals
        # =====================================================
