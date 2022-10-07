from django.apps import AppConfig


class AchievementsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lms.achievements'

    def ready(self):
        import lms.achievements.signals
