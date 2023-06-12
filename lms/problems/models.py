from django.db import models
from lms.steps.models import Step
from django.urls import reverse
from users.models import CustomUser
from lms.steps.models import DefaultStepManager
from lms.lessons.models import Lesson


class ProblemStep(Step):
    input_format = models.TextField(
        verbose_name='Формат ввода',
        max_length=10000,
        blank=True,
    )
    output_format = models.TextField(
        verbose_name='Формат вывода',
        max_length=10000,
        blank=True,
    )
    notes = models.TextField(
        verbose_name='Примечания',
        max_length=10000,
        blank=True,
    )
    start_code = models.TextField(
        verbose_name='Дополнительный код',
        max_length=10000,
        blank=True,
        default='',
    )
    first_sample = models.IntegerField(
        verbose_name='Первый сэмпл',
        default=1,
    )
    last_sample = models.IntegerField(
        verbose_name='Последний сэмпл',
        default=3,
    )
    first_test = models.IntegerField(
        verbose_name='Первый тест',
        default=4,
    )
    cputime = models.IntegerField(
        verbose_name='CPU Time',
        default=1,
    )
    memory = models.IntegerField(
        verbose_name='Memory',
        default=64,
    )
    num_attempts = models.IntegerField(
        verbose_name='Количество попыток',
        default=-1,
    )
    objects = DefaultStepManager()

    class Meta:
        verbose_name = 'Задача на программирование'
        verbose_name_plural = '1. Задачи на программирование'
        ordering = ['pk']

    def get_cms_detail_url(self):
        lesson: Lesson = self.connections.first().lesson
        return reverse(
            'CMS_ProblemStepDetail',
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
            'CMS_ProblemStepUpdate',
            kwargs={
                'course_slug': lesson.topic.course.slug,
                'topic_slug': lesson.topic.slug,
                'lesson_slug': lesson.slug,
                'step_slug': self.slug,
            },
        )

    def icon_class(self):
        return 'bi-code-square'


class TestForProblemStep(models.Model):
    input = models.TextField(
        verbose_name='Входные данные',
        max_length=100000,
        blank=True,
    )
    output = models.TextField(
        verbose_name='Выходные данные',
        max_length=100000,
        blank=True,
    )
    problem = models.ForeignKey(
        ProblemStep,
        related_name='tests',
        verbose_name='Задача',
        on_delete=models.CASCADE,
    )
    number = models.IntegerField(
        verbose_name='№ теста',
        default=1000,
    )

    class Meta:
        verbose_name = 'Тест для задач'
        verbose_name_plural = '2. Тесты для задач'
        ordering = ['pk']
        unique_together = ('problem', 'number')


class UserAnswerForProblemStep(models.Model):
    code = models.TextField(
        verbose_name='Код пользователя',
        max_length=10000,
    )
    user = models.ForeignKey(
        CustomUser,
        related_name='codes',
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
    )
    problem = models.ForeignKey(
        ProblemStep,
        related_name='codes',
        verbose_name='Задача',
        on_delete=models.CASCADE,
    )
    date_create = models.DateTimeField(
        auto_now_add=True,
    )
    date_update = models.DateTimeField(
        auto_now=True,
    )
    LANGUAGE_CHOICES = [
        ('python', 'Python'),
        ('cpp', 'C++'),
    ]
    language = models.CharField(
        verbose_name='Язык программирования',
        max_length=10,
        choices=LANGUAGE_CHOICES,
        default='python',
    )
    VERDICT_CHOICES = [
        ('PR', 'На проверке'),
        ('OK', 'OK'),
        ('CE', 'Ошибка компиляции'),
        ('WA', 'Неправильный ответ'),
        ('TL', 'Превышение времени'),
        ('ML', 'Превышение памяти'),
        ('UN', 'Незвестная ошибка'),
    ]
    verdict = models.CharField(
        verbose_name='Вердикт',
        max_length=2,
        choices=VERDICT_CHOICES,
        default='PR',
    )
    cputime = models.FloatField(
        verbose_name='CPU Time',
        default=0,
    )
    first_fail_test = models.IntegerField(
        verbose_name='Первый ошибочный тест',
        default=0,
    )
    points = models.IntegerField(
        verbose_name='Баллы',
        default=0,
    )
    is_new = models.BooleanField(
        verbose_name='Новая?',
        default=True
    )

    class Meta:
        verbose_name = 'Попытка пользователя'
        verbose_name_plural = '3. Попытки пользователей'
        ordering = ['pk']

    def get_lms_detail_url(self):
        return reverse(
            'LMS_UserCodeDetail',
            kwargs={
                'user_answer_pk': self.pk,
            },
        )

    def get_retest_url(self):
        return reverse(
            'rerun_submissions',
            kwargs={
                'user_answer_pk': self.pk,
            }
        )


class TestUserAnswer(models.Model):
    user = models.ForeignKey(
        CustomUser,
        related_name='attempts',
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
    )
    code = models.ForeignKey(
        UserAnswerForProblemStep,
        related_name='attempts',
        verbose_name='Решение',
        on_delete=models.CASCADE,
    )
    test = models.ForeignKey(
        TestForProblemStep,
        related_name='attempts',
        verbose_name='Тест',
        on_delete=models.CASCADE,
    )

    VERDICT_CHOICES = [
        ('PR', 'На проверке'),
        ('OK', 'OK'),
        ('CE', 'Ошибка компиляции'),
        ('WA', 'Неправильный ответ'),
        ('TL', 'Превышение времени'),
        ('ML', 'Превышение памяти'),
        ('UN', 'Незвестная ошибка'),
    ]
    verdict = models.CharField(
        verbose_name='Вердикт',
        max_length=2,
        choices=VERDICT_CHOICES,
        default='WA',
    )
    date_create = models.DateTimeField(
        auto_now_add=True,
    )
    date_update = models.DateTimeField(
        auto_now=True,
    )

    exit_code = models.IntegerField(
        verbose_name='exit_code',
    )
    stdout = models.TextField(
        verbose_name='stdout',
        max_length=10000,
    )
    stderr = models.TextField(
        verbose_name='stderr',
        max_length=10000,
    )
    duration = models.FloatField(
        verbose_name='duration',
        default=0,
    )
    timeout = models.BooleanField(
        verbose_name='timeout',
        default=False,
    )
    oom_killed = models.BooleanField(
        verbose_name='oom_killed',
        default=False,
    )

    class Meta:
        verbose_name = 'Результат теста'
        verbose_name_plural = '4. Результаты тестов'
        ordering = ['pk']
