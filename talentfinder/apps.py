from django.apps import AppConfig


class TalentfinderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'talentfinder'
    verbose_name = 'Talent Finder'

    def ready(self):
        """Import signals when app is ready"""
        pass
