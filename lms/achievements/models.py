from django.db import models
from polymorphic.models import PolymorphicModel
from lms.courses.models import Course
from lms.lessons.models import Lesson
from lms.topics.models import Topic
from users.models import CustomUser
from lms.steps.models import Step


class Achievement(PolymorphicModel):
    user = models.ForeignKey(
        CustomUser,
        related_name='achievements',
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
    )
    date_create = models.DateTimeField(
        auto_now=True,
    )
    date_update = models.DateTimeField(
        auto_now=True,
    )
    points = models.PositiveIntegerField(
        verbose_name='Полученные баллы',
        default=0,
    )

    class Meta:
        verbose_name = 'Достижение'
        verbose_name_plural = 'Достижения'
        ordering = ['pk']


class StepAchievement(Achievement):
    for_what = models.ForeignKey(
        Step,
        related_name='step_achievements',
        verbose_name='Шаг',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Достижение за шаг'
        verbose_name_plural = 'Достижения за шаги'
        ordering = ['pk']


class CourseAchievement(Achievement):
    for_what = models.ForeignKey(
        Course,
        related_name='course_achievements',
        verbose_name='Курс',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Достижение за курс'
        verbose_name_plural = 'Достижения за курсы'
        ordering = ['pk']
