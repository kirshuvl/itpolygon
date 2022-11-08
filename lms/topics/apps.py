from django.apps import AppConfig


class TopicsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lms.topics'

    def ready(self):
        import lms.topics.signals
