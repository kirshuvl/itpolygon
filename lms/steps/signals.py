from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from lms.assignment.models import UserAnswerForAssignmentStep
from lms.steps.models import Step, StepEnroll,LessonStepConnection, TextStep
from lms.achievements.models import StepAchievement
from lms.lessons.models import Lesson

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
    pass
    #steps = Step.objects.filter(
    #    lesson__slug=instance.lesson.slug).order_by('number')
    #for num, step in enumerate(steps):
    #    step.number = num + 1
    #    step.save()


@receiver(post_save, sender=UserAnswerForAssignmentStep)
def change_status(sender, instance, **kwargs):
    if instance.is_correct:
        step_enroll = StepEnroll.objects.get(user=instance.user,
                                             step=instance.assignment)
        step_enroll.status = 'OK'
        step_enroll.save()

@receiver(post_save, sender=TextStep)
def create_connection(sender, instance, created, **kwargs):
    print(kwargs)

@receiver(post_delete, sender=LessonStepConnection)
def delete_connection(sender, instance, **kwargs):
    lesson = Lesson.objects.get(slug=instance.lesson.slug)
    connections = LessonStepConnection.objects.filter(lesson=lesson).order_by('number')

    for el, connect in enumerate(connections):
        connect.number = el + 1
        connect.save()