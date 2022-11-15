from django.db import models
from users.models import CustomUser
from lms.lessons.models import Lesson
from lms.steps.models import Step
from lms.courses.models import Course
# Create your models here.
import datetime


class Homework(models.Model):
    description = models.TextField(
        verbose_name='Описание',
        max_length=10000,
    )
    user = models.ForeignKey(
        CustomUser,
        related_name='user_homeworks',
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
    )
    date_create = models.DateTimeField(
        auto_now=True,
    )
    date_update = models.DateTimeField(
        auto_now=True,
    )
    date_to = models.DateTimeField(
    )
    course = models.ForeignKey(
        Course,
        related_name='course_homeworks',
        verbose_name='Курс',
        on_delete=models.CASCADE,
    )
    steps = models.ManyToManyField(
        Step,
        related_name='step_homeworks',
        verbose_name='Шаги',
    )
    is_done = models.BooleanField(
        verbose_name='Сдано?',
        default=False,
    )

    class Meta:
        verbose_name = 'Домашнее задание'
        verbose_name_plural = 'Домашние задания'
        ordering = ['pk']

    def get_time_left(self):

        def get_day(day_count):
            if day_count == 1:
                return 'день'
            elif day_count in (2, 3, 4):
                return 'дня'
            else:
                return 'дней'
        date_from = datetime.datetime.strptime(
            str(self.date_to)[:-6], "%Y-%m-%d %H:%M:%S")
        date_to = datetime.datetime.now()
        difference = date_from - date_to
        print(difference.days)

        return '{} {}'.format(abs(difference.days), get_day(abs(difference.days)))

    def is_user_late(self):
        date_from = datetime.datetime.strptime(
            str(self.date_to)[:-6], "%Y-%m-%d %H:%M:%S")
        date_to = datetime.datetime.now()
        difference = date_from - date_to
        if difference.seconds < 0 or difference.days < 0:
            return True

        return False
