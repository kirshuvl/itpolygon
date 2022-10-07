from django.dispatch import receiver
from django.db.models.signals import pre_delete
from lms.achievements.models import Achievement


@receiver(pre_delete, sender=Achievement)
def pre_delete_achievement(instance, **kwargs):
    points = instance.points
    user = instance.user
    user.coin -= points
    user.save()
