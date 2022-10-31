from django.dispatch import receiver
from django.db.models.signals import post_save
from lms.steps.models import StepEnroll
from lms.achievements.models import StepAchievement


@receiver(post_save, sender=StepEnroll)
def create_achievement(sender, instance, **kwargs):
    if instance.status == 'OK':
        achieve = StepAchievement.objects.get_or_create(
            user=instance.user,
            points=instance.step.points,
            for_what=instance.step,
        )
