from django.apps import AppConfig


class CampsiteappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'CampSiteApp'

    def ready(self):
        import CampSiteApp.signals

