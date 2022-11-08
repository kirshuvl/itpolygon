from django.dispatch import receiver
from django.db.models.signals import post_delete
from lms.lessons.models import Lesson




@receiver(post_delete, sender=Lesson)
def delete_lesson(sender, instance, **kwargs):
    lessons = Lesson.objects.filter(
        topic__slug=instance.topic.slug).order_by('number')
    for num, lesson in enumerate(lessons):
        lesson.number = num + 1
        lesson.save()
