from django.db import models
from users.models import CustomUser
from lms.topics.models import Topic
from django.urls import reverse


class Lesson(models.Model):
    title = models.CharField(
        verbose_name='Название урока',
        max_length=50,
    )
    slug = models.SlugField(
        verbose_name='Slug',
        max_length=25,
        unique=True,
    )
    description = models.TextField(
        verbose_name='Описание урока',
        max_length=1000,
    )
    is_published = models.BooleanField(
        verbose_name='Опубликовать?',
        default=False,
    )
    date_create = models.DateTimeField(
        auto_now_add=True,
    )
    date_update = models.DateTimeField(
        auto_now=True,
    )
    number = models.IntegerField(
        verbose_name='№ урока в теме',
        default=1000,
    )
    topic = models.ForeignKey(
        Topic,
        related_name='lessons',
        verbose_name='Тема',
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        CustomUser,
        related_name='lessons',
        verbose_name='Автор урока',
        on_delete=models.CASCADE,
    )

    LESSON_TYPE = [
        ('ST', 'Обычный урок'),
        ('QZ', 'Урок - тест'),
        ('CT', 'Контест'),
    ]
    type = models.CharField(
        verbose_name='Тип урока',
        max_length=2,
        choices=LESSON_TYPE,
        default='ST'
    )

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ['pk']

    def __str__(self):
        return self.title

    def get_lms_url(self):
        return reverse(
            'LMS_LessonDetail',
            kwargs={
                'course_slug': self.topic.course.slug,
                'topic_slug': self.topic.slug,
                'lesson_slug': self.slug,
            },
        )

    def get_cms_url(self):
        return reverse(
            'CMS_LessonDetail',
            kwargs={
                'course_slug': self.topic.course.slug,
                'topic_slug': self.topic.slug,
                'lesson_slug': self.slug,
            }
        )
    
    def get_stat_url(self):
        return reverse(
            'LessonStatistics',
            kwargs={
                'lesson_slug': self.slug,
            },
        )
    
    def get_course_lms_url(self):
        return self.topic.course.get_lms_url()
    
    

    '''

    def get_statistics(self):
        return reverse(
            'LessonStatistics',
            kwargs={
                'lesson_slug': self.slug,
            },
        )

    def end_lesson(self):
        return reverse(
            'UserEndLesson',
            kwargs={
                'course_slug': self.topic.course.slug,
                'topic_slug': self.topic.slug,
                'lesson_slug': self.slug,
            },
        )

    def icon(self):
        if self.type == 'ST':
            return 'bi-card-text'
        elif self.type == 'QZ':
            return 'bi-question-square'
        else:
            return 'bi-code-square'

    def down(self):
        return reverse(
            'CMS_LessonDown',
            kwargs={
                'course_slug': self.topic.course.slug,
                'topic_slug': self.topic.slug,
                'lesson_slug': self.slug,
            },
        )

    def up(self):
        return reverse(
            'CMS_LessonUp',
            kwargs={
                'course_slug': self.topic.course.slug,
                'topic_slug': self.topic.slug,
                'lesson_slug': self.slug,
            },
        )

    def set_is_published(self):
        return reverse(
            'lesson_check_publish',
            kwargs={
                'lesson_slug': self.slug,
            },
        )

    def get_update_url(self):
        return reverse(
            'CMS_LessonUpdate',
            kwargs={
                'course_slug': self.topic.course.slug,
                'topic_slug': self.topic.slug,
                'lesson_slug': self.slug,
            },
        )

    def get_delete_url(self):
        return reverse(
            'CMS_LessonDelete',
            kwargs={
                'course_slug': self.topic.course.slug,
                'topic_slug': self.topic.slug,
                'lesson_slug': self.slug,
            },
        )'''
