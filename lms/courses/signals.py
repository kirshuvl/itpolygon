from django.dispatch import receiver
from django.db.models.signals import post_save
from lms.courses.models import CourseEnroll
from lms.topics.models import TopicEnroll
from lms.lessons.models import LessonEnroll


@receiver(post_save, sender=CourseEnroll)
def post_save_course_enroll(instance, created, **kwargs):
    if created:
        course = instance.course
        user = instance.user
        first_topic = course.topics.order_by('number').first()
        first_lesson = first_topic.lessons.order_by('number').first()
        topic_enroll = TopicEnroll(topic=first_topic, user=user)
        lesson_enroll = LessonEnroll(lesson=first_lesson, user=user)

        topic_enroll.save()
        lesson_enroll.save()
