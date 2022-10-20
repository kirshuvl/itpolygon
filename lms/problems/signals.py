from django.dispatch import receiver
from django.db.models.signals import post_save
from lms.problems.models import UserAnswerForProblemStep
from lms.problems.tasks import run_user_code


@receiver(post_save, sender=UserAnswerForProblemStep)
def post_save_user_asnwer(sender, instance, created, **kwargs):
    if created:
        run_user_code.delay(instance.pk)
