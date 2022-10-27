from statistics import mode
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
    points = models.PositiveIntegerField(
        verbose_name='Баллы за пройденный урок',
        default=0,
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

    def get_absolute_url(self):
        return reverse(
            'LessonDetail',
            kwargs={
                'course_slug': self.topic.course.slug,
                'topic_slug': self.topic.slug,
                'lesson_slug': self.slug,
            },
        )

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
    

    def get_cms_url(self):
        return reverse(
            'CMS_LessonDetail',
            kwargs={
                'course_slug': self.topic.course.slug,
                'topic_slug': self.topic.slug,
                'lesson_slug': self.slug,
            }
        )


class LessonEnroll(models.Model):
    lesson = models.ForeignKey(
        Lesson,
        related_name='lessons_enrolls',
        verbose_name='Урок',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        CustomUser,
        related_name='lessons_enrolls',
        verbose_name='Пользователь',
        on_delete=models.CASCADE
    )
    date_create = models.DateTimeField(
        auto_now=True
    )
    date_update = models.DateTimeField(
        auto_now=True,
    )
    STATUS_CHOICES = [
        ('PR', 'Урок изучается'),
        ('RP', 'Урок повторяется'),
        ('WA', 'Урок не сдан'),
        ('OK', 'Урок пройден'),
    ]
    status = models.CharField(
        verbose_name='Статус',
        max_length=2,
        choices=STATUS_CHOICES,
        default='PR'
    )

    class Meta:
        verbose_name = 'Зачисление на урок'
        verbose_name_plural = 'Зачисления на уроки'
        ordering = ['pk']
        unique_together = ('lesson', 'user')

    def get_absolute_url(self):
        return reverse(
            'LessonDetail',
            kwargs={
                'course_slug': self.topic.course.slug,
                'topic_slug': self.topic.slug,
                'lesson_slug': self.slug,
            },
        )
