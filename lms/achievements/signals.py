from django.dispatch import receiver
from django.db.models.signals import pre_delete, post_save
from lms.achievements.models import StepAchievement


@receiver(pre_delete, sender=StepAchievement)
def pre_delete_achievement(sender, instance, **kwargs):
    user = instance.user
    points = instance.points
    user.coin -= points
    user.save()


@receiver(post_save, sender=StepAchievement)
def post_save_achievement(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        points = instance.points
        user.coin += points
        user.save()
