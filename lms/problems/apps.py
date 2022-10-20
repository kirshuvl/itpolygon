from django.apps import AppConfig


class ProblemsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lms.problems'

    def ready(self):
        import lms.problems.signals
