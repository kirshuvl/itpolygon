from django.db import models
from django.urls import reverse
from lms.lessons.models import Lesson
from lms.steps.models import Step, DefaultStepManager
from users.models import CustomUser


class AssignmentStep(Step):
    file = models.FileField(
        verbose_name='Файл',
        upload_to='assignment/%Y/%m/%d/',
        blank=True,
    )
    objects = DefaultStepManager()

    class Meta:
        verbose_name = 'Задание'
        verbose_name_plural = '1. Задания'
        ordering = ['title']

    def get_cms_detail_url(self):
        lesson: Lesson = self.connections.first().lesson

        return reverse(
            'CMS_AssignmentStepDetail',
            kwargs={
                'course_slug': lesson.topic.course.slug,
                'topic_slug': lesson.topic.slug,
                'lesson_slug': lesson.slug,
                'step_slug': self.slug,
            },
        )

    def get_cms_update_url(self):
        lesson: Lesson = self.connections.first().lesson

        return reverse(
            'CMS_AssignmentStepUpdate',
            kwargs={
                'course_slug': lesson.topic.course.slug,
                'topic_slug': lesson.topic.slug,
                'lesson_slug': lesson.slug,
                'step_slug': self.slug,
            },
        )

    def icon_class(self):
        return 'bi-clipboard-plus'


class UserAnswerForAssignmentStep(models.Model):
    user_answer = models.TextField(
        verbose_name='Ответ пользователя',
        max_length=10000,
    )
    is_correct = models.BooleanField(
        default=False,
    )
    user = models.ForeignKey(
        CustomUser,
        related_name='assignment_answers',
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
    )
    assignment = models.ForeignKey(
        AssignmentStep,
        related_name='assignment_answers',
        verbose_name='Задание',
        on_delete=models.CASCADE,
    )
    date_create = models.DateTimeField(
        auto_now=True,
    )
    date_update = models.DateTimeField(
        auto_now=True,
    )
    file = models.FileField(
        verbose_name='Файл',
        upload_to='assignment/%Y/%m/%d/',
        blank=True,
    )
    STATUS_CHOICES = [
        ('RV', 'На проверке'),
        ('BF', 'На доработке'),
        ('OK', 'Проверено'),
    ]
    status = models.CharField(
        verbose_name='Статус',
        max_length=2,
        choices=STATUS_CHOICES,
        default='RV',
    )

    def __str__(self) -> str:
        return self.assignment.title

    class Meta:
        verbose_name = 'Ответ на задание'
        verbose_name_plural = '2. Ответы на задания'
        ordering = ['pk']


class ReviewForUserAnswerForAssignmentStep(models.Model):
    user = models.ForeignKey(
        CustomUser,
        related_name='reviews',
        verbose_name='Автор ревью',
        on_delete=models.PROTECT,
    )
    user_answer = models.ForeignKey(
        UserAnswerForAssignmentStep,
        related_name='reviews',
        verbose_name='Задание',
        on_delete=models.CASCADE,
    )
    text = models.TextField(
        verbose_name='Ответ на решение',
        max_length=10000,
    )
    date_create = models.DateTimeField(
        auto_now=True,
    )
    date_update = models.DateTimeField(
        auto_now=True,
    )
    file = models.FileField(
        verbose_name='Файл',
        upload_to='assignment/%Y/%m/%d/',
        blank=True,
    )

    class Meta:
        verbose_name = 'Ревью задания'
        verbose_name_plural = '3. Ревью заданий'
        ordering = ['pk']
