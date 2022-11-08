from django.dispatch import receiver
from django.db.models.signals import post_delete
from lms.topics.models import Topic




@receiver(post_delete, sender=Topic)
def delete_topic(sender, instance, **kwargs):
    topics = Topic.objects.filter(
        course__slug=instance.course.slug).order_by('number')

    for num, topic in enumerate(topics):
        topic.number = num + 1
        topic.save()
