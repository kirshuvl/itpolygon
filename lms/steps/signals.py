from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from lms.steps.models import Step, StepEnroll
from lms.achievements.models import StepAchievement


@receiver(post_save, sender=StepEnroll)
def create_achievement(sender, instance, **kwargs):
    if instance.status == 'OK':
        achieve = StepAchievement.objects.get_or_create(
            user=instance.user,
            points=instance.step.points,
            for_what=instance.step,
        )


@receiver(post_delete, sender=Step)
def delete_step(sender, instance, **kwargs):
    steps = Step.objects.filter(
        lesson__slug=instance.lesson.slug).order_by('number')
    for num, step in enumerate(steps):
        step.number = num + 1
        step.save()
