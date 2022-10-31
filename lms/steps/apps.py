from django.apps import AppConfig


class StepsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lms.steps'

    def ready(self):
        import lms.steps.signals
