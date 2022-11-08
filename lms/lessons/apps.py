from django.apps import AppConfig


class LessonsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lms.lessons'

    def ready(self):
        import lms.lessons.signals
