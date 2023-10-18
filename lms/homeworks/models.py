from django.db import models
from users.models import CustomUser
from lms.lessons.models import Lesson
from lms.steps.models import Step
from lms.courses.models import Course
import datetime
from django.urls import reverse


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

    author = models.ForeignKey(
        CustomUser,
        related_name='homeworks',
        verbose_name='Автор шага',
        on_delete=models.CASCADE,
    )
    course = models.ForeignKey(
        Course,
        related_name='course_homeworks',
        verbose_name='Курс',
        on_delete=models.CASCADE,
    )
    is_done = models.BooleanField(
        verbose_name='Сдано?',
        default=False,
    )

    class Meta:
        verbose_name = 'Домашнее задание'
        verbose_name_plural = 'Домашние задания'
        ordering = ['pk']

    def __str__(self) -> str:
        return f'Домашнее задание № {self.pk}'

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

    def get_lms_detail_url(self):
        return reverse(
            'LMS_UserHomeworkDetail',
            kwargs={
                'course_slug': self.course.slug,
                'pk': self.pk
            }
        )

    def get_steps_cnt(self):

        return self.h_connections.count()

    def get_user_end_steps(self):

        cnt = 0

        for connect in self.h_connections.all():
            enrolls = connect.step.steps_enrolls.all()
            if enrolls.count() > 1:
                return 'Error'
            enroll = connect.step.steps_enrolls.first()
            if enroll is not None and enroll.status == 'OK':
                cnt += 1

        return cnt

    def get_user_percentage(self):
        if self.get_steps_cnt() == 0:
            return 0

        return int(self.get_user_end_steps() / self.get_steps_cnt() * 100)


class HomeworkStepConnection(models.Model):
    number = models.IntegerField(
        verbose_name='№ шага в уроке',
        default=1000,
    )
    homework = models.ForeignKey(
        Homework,
        related_name='h_connections',
        verbose_name='Урок',
        on_delete=models.CASCADE,
    )
    step = models.ForeignKey(
        Step,
        related_name='h_connections',
        verbose_name='Шаг',
        on_delete=models.CASCADE,
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
    num_attempts = models.IntegerField(
        verbose_name='Количество попыток',
        default=-1,
    )

    class Meta:
        verbose_name = 'ДЗ - Шаги'
        verbose_name_plural = 'ДЗ - Шаги'
        ordering = ['pk']
