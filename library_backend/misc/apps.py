from django.apps import AppConfig


class MiscConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'misc'
    
    def ready(self) -> None:
        import misc.signals
