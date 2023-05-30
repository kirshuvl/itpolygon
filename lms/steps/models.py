from django.db import models
from django.db.models.query import QuerySet
from users.models import CustomUser
from lms.lessons.models import Lesson
from django.urls import reverse
from polymorphic.models import PolymorphicModel


class StepManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('textstep', 'videostep', 'questionstep', 'questionchoicestep', 'assignmentstep', 'problemstep')


class DefaultStepManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


class Step(models.Model):
    title = models.CharField(
        verbose_name='Название шага',
        max_length=50,
    )
    slug = models.SlugField(
        verbose_name='Slug',
        max_length=50,
        unique=True,
    )
    description = models.TextField(
        verbose_name='Описание шага',
        max_length=100000,
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
        verbose_name='№ шага в уроке',
        default=1000,
    )
    author = models.ForeignKey(
        CustomUser,
        related_name='steps',
        verbose_name='Автор шага',
        on_delete=models.CASCADE,
    )
    points = models.PositiveIntegerField(
        verbose_name='Баллы за пройденный шаг',
        default=1,
    )
    lesson = models.ForeignKey(
        Lesson,
        related_name='steps',
        verbose_name='Урок',
        on_delete=models.CASCADE,
    )
    objects = StepManager()

    def __str__(self):
        return self.title

    # @property
    def video_url(self):
        if hasattr(self, 'videostep'):
            return self.videostep.video_url
        return None

    class Meta:
        verbose_name = 'Шаг урока'
        verbose_name_plural = 'Шаги уроков'
        ordering = ['title']

    def icon_class(self):
        if hasattr(self, 'textstep'):
            return 'bi-card-text'
        elif hasattr(self, 'videostep'):
            return 'bi-play-btn'
        elif hasattr(self, 'questionstep'):
            return 'bi-question-square'
        elif hasattr(self, 'questionchoicestep'):
            return 'bi-question-square'
        elif hasattr(self, 'assignmentstep'):
            return 'bi-clipboard-plus'
        elif hasattr(self, 'problemstep'):
            return 'bi-code-square'

    def enroll_color(self):
        enroll = self.steps_enrolls.first()
        if enroll is None:
            return 'secondary'
        if enroll.status == 'OK':
            return 'success'
        if enroll.status == 'PR':
            return 'primary'
        elif enroll.status == 'RP':
            return 'warning'
        elif enroll.status == 'WA':
            return 'danger'
        return 'secondary'

    def get_lms_url(self):
        lesson: Lesson = self.connections.first().lesson
        if hasattr(self, 'textstep'):
            url = 'LMS_TextStepDetail'
        elif hasattr(self, 'videostep'):
            url = 'LMS_VideoStepDetail'
        elif hasattr(self, 'questionstep'):
            url = 'LMS_QuestionStepDetail'
        elif hasattr(self, 'questionchoicestep'):
            url = 'LMS_QuestionChoiceStepDetail'
        elif hasattr(self, 'assignmentstep'):
            url = 'ProblemStepDetail'
        elif hasattr(self, 'problemstep'):
            url = 'AssignmentStepDetail'
        else:
            return '#'

        return reverse(
            url,
            kwargs={
                'course_slug': lesson.topic.course.slug,
                'topic_slug': lesson.topic.slug,
                'lesson_slug': lesson.slug,
                'step_slug': self.slug,
            },
        )

    def get_type(self):
        if hasattr(self, 'textstep'):
            return 'textstep'
        elif hasattr(self, 'videostep'):
            return 'videostep'
        elif hasattr(self, 'questionstep'):
            return 'questionstep'
        elif hasattr(self, 'questionchoicestep'):
            return 'questionchoicestep'
        elif hasattr(self, 'assignmentstep'):
            return 'assignmentstep'
        elif hasattr(self, 'problemstep'):
            return 'problemstep'
        return 'None'

    def get_current_lesson(self):
        lesson: Lesson = self.connections.first().lesson
        return lesson

    def end_step(self):
        lesson: Lesson = self.connections.first().lesson
        return reverse(
            'UserEndStep',
            kwargs={
                'course_slug': lesson.topic.course.slug,
                'topic_slug': lesson.topic.slug,
                'lesson_slug': lesson.slug,
                'step_slug': self.slug,
            },
        )

    def cms_delete(self):
        return reverse(
            'CMS_StepDelete',
            kwargs={
                'course_slug': self.lesson.topic.course.slug,
                'topic_slug': self.lesson.topic.slug,
                'lesson_slug': self.lesson.slug,
                'step_slug': self.slug,
            },
        )


class LessonStepConnectionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('lesson__topic__course')


class LessonStepConnection(models.Model):
    number = models.IntegerField(
        verbose_name='№ шага в уроке',
        default=1000,
    )
    author = models.ForeignKey(
        CustomUser,
        related_name='author',
        verbose_name='Автор шага',
        on_delete=models.CASCADE,
    )
    lesson = models.ForeignKey(
        Lesson,
        related_name='connections',
        verbose_name='Урок',
        on_delete=models.CASCADE,
    )
    step = models.ForeignKey(
        Step,
        related_name='connections',
        verbose_name='Шаг',
        on_delete=models.CASCADE,
    )
    is_published = models.BooleanField(
        verbose_name='Опубликовать?',
        default=False,
    )
    objects = LessonStepConnectionManager()

    class Meta:
        verbose_name = 'Шаг - Урок'
        verbose_name_plural = '0. Шаги - Уроки'
        ordering = ['lesson', 'step', 'number']
        unique_together = ('lesson', 'step')

    def connect_up(self):
        return reverse(
            'connect_up',
            kwargs={
                'lesson_slug': self.lesson.slug,
                'pk': self.pk,
            }
        )

    def connect_down(self):
        return reverse(
            'connect_down',
            kwargs={
                'lesson_slug': self.lesson.slug,
                'pk': self.pk,
            }
        )


class TextStep(Step):
    text = models.TextField(
        verbose_name='Текст'
    )
    objects = DefaultStepManager()

    class Meta:
        verbose_name = 'Текстовый шаг'
        verbose_name_plural = '1. Текстовые шаги'
        ordering = ['pk']

    def get_lms_url(self, **kwargs):
        lesson: Lesson = self.connections.first().lesson
        return reverse(
            'LMS_TextStepDetail',
            kwargs={
                'course_slug': lesson.topic.course.slug,
                'topic_slug': lesson.topic.slug,
                'lesson_slug': lesson.slug,
                'step_slug': self.slug,
            },
        )

    def get_absolute_url(self):
        return reverse(
            'TextStepDetail',
            kwargs={
                'course_slug': self.lesson.topic.course.slug,
                'topic_slug': self.lesson.topic.slug,
                'lesson_slug': self.lesson.slug,
                'step_slug': self.slug,
            },
        )

    def get_cms_url(self):
        return reverse(
            'CMS_TextStepDetail',
            kwargs={
                'course_slug': self.lesson.topic.course.slug,
                'topic_slug': self.lesson.topic.slug,
                'lesson_slug': self.lesson.slug,
                'step_slug': self.slug,
            },
        )

    def cms_update(self):
        return reverse(
            'CMS_TextStepUpdate',
            kwargs={
                'course_slug': self.lesson.topic.course.slug,
                'topic_slug': self.lesson.topic.slug,
                'lesson_slug': self.lesson.slug,
                'step_slug': self.slug,
            },
        )


class VideoStep(Step):
    video_url = models.URLField(
        verbose_name='Ссылка на видео',
        max_length=500,
    )
    objects = DefaultStepManager()

    class Meta:
        verbose_name = 'Видео шаг'
        verbose_name_plural = '2. Видео шаги'
        ordering = ['title']

    def get_absolute_url(self):
        return reverse(
            'VideoStepDetail',
            kwargs={
                'course_slug': self.lesson.topic.course.slug,
                'topic_slug': self.lesson.topic.slug,
                'lesson_slug': self.lesson.slug,
                'step_slug': self.slug,
            },
        )

    def get_cms_url(self):
        return reverse(
            'CMS_VideoStepDetail',
            kwargs={
                'course_slug': self.lesson.topic.course.slug,
                'topic_slug': self.lesson.topic.slug,
                'lesson_slug': self.lesson.slug,
                'step_slug': self.slug,
            },
        )

    def cms_update(self):
        return reverse(
            'CMS_VideoStepUpdate',
            kwargs={
                'course_slug': self.lesson.topic.course.slug,
                'topic_slug': self.lesson.topic.slug,
                'lesson_slug': self.lesson.slug,
                'step_slug': self.slug,
            },
        )


class QuestionStep(Step):
    answer = models.CharField(
        verbose_name='Правильный ответ',
        max_length=250,
    )
    num_attempts = models.IntegerField(
        verbose_name='Количество попыток',
        default=-1,
    )
    objects = DefaultStepManager()

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = '3. Вопросы'
        ordering = ['title']

    def get_absolute_url(self):
        return reverse(
            'QuestionStepDetail',
            kwargs={
                'course_slug': self.lesson.topic.course.slug,
                'topic_slug': self.lesson.topic.slug,
                'lesson_slug': self.lesson.slug,
                'step_slug': self.slug,
            },
        )

    def get_cms_url(self):
        return reverse(
            'CMS_QuestionStepDetail',
            kwargs={
                'course_slug': self.lesson.topic.course.slug,
                'topic_slug': self.lesson.topic.slug,
                'lesson_slug': self.lesson.slug,
                'step_slug': self.slug,
            },
        )

    def cms_update(self):
        return reverse(
            'CMS_QuestionStepUpdate',
            kwargs={
                'course_slug': self.lesson.topic.course.slug,
                'topic_slug': self.lesson.topic.slug,
                'lesson_slug': self.lesson.slug,
                'step_slug': self.slug,
            },
        )

    def type(self):
        return 'question'

    def get_type(self):
        return 'videostep'


class UserAnswerForQuestionStep(models.Model):
    user_answer = models.CharField(
        verbose_name='Ответ пользователя',
        max_length=30,
    )
    is_correct = models.BooleanField(
        default=False,
    )
    user = models.ForeignKey(
        CustomUser,
        related_name='question_answers',
        verbose_name='Пользователь',
        on_delete=models.PROTECT,
    )
    question = models.ForeignKey(
        QuestionStep,
        related_name='question_answers',
        verbose_name='Вопрос',
        on_delete=models.CASCADE,
    )
    date_create = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        verbose_name = 'Ответ пользователя'
        verbose_name_plural = 'Ответы пользователя'
        ordering = ['pk']

    def get_absolute_url(self):
        lesson: Lesson = self.connections.first().lesson
        return reverse(
            'LMS_QuestionStepDetail',
            kwargs={
                'course_slug': lesson.topic.course.slug,
                'topic_slug': lesson.topic.slug,
                'lesson_slug': lesson.slug,
                'step_slug': self.question.slug,
            },
        )


class QuestionChoiceStep(Step):
    num_attempts = models.IntegerField(
        verbose_name='Количество попыток',
        default=-1,
    )

    class Meta:
        verbose_name = 'Вопрос с выбором ответа'
        verbose_name_plural = 'Вопросы с выбором ответа'
        ordering = ['title']

    def get_absolute_url(self):
        return reverse(
            'QuestionChoiceStepDetail',
            kwargs={
                'course_slug': self.lesson.topic.course.slug,
                'topic_slug': self.lesson.topic.slug,
                'lesson_slug': self.lesson.slug,
                'step_slug': self.slug,
            },
        )


class TestForQuestionChoiceStep(models.Model):
    title = models.CharField(
        verbose_name='Ответ',
        max_length=250,
    )
    is_correct = models.BooleanField(
        default=False,
    )
    question = models.ForeignKey(
        QuestionChoiceStep,
        related_name='tests',
        verbose_name='Вопрос',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответа'
        ordering = ['pk']

    def __str__(self) -> str:
        return self.title


class UserAnswerForQuestionChoiceStep(models.Model):
    user_answer = models.ForeignKey(
        TestForQuestionChoiceStep,
        related_name='answers',
        verbose_name='Ответ пользователя',
        on_delete=models.PROTECT,
    )
    is_correct = models.BooleanField(
        default=False,
    )
    user = models.ForeignKey(
        CustomUser,
        related_name='question_choice_answers',
        verbose_name='Пользователь',
        on_delete=models.PROTECT,
    )
    question = models.ForeignKey(
        QuestionChoiceStep,
        related_name='answers',
        verbose_name='Вопрос',
        on_delete=models.CASCADE,
    )
    date_create = models.DateTimeField(
        auto_now=True,
    )

    def get_absolute_url(self):
        return reverse(
            'QuestionChoiceStepDetail',
            kwargs={
                'course_slug': self.question.lesson.topic.course.slug,
                'topic_slug': self.question.lesson.topic.slug,
                'lesson_slug': self.question.lesson.slug,
                'step_slug': self.question.slug,
            },
        )


class StepEnroll(models.Model):
    step = models.ForeignKey(
        Step,
        related_name='steps_enrolls',
        verbose_name='Шаг',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        CustomUser,
        related_name='steps_enrolls',
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
    )
    date_create = models.DateTimeField(
        auto_now_add=True,
    )
    date_update = models.DateTimeField(
        auto_now=True,
    )
    STATUS_CHOICES = [
        ('PR', 'Шаг изучается'),
        ('RP', 'Шаг повторяется'),
        ('WA', 'Шаг не сдан'),
        ('OK', 'Шаг пройден'),
    ]
    status = models.CharField(
        verbose_name='Статус',
        max_length=2,
        choices=STATUS_CHOICES,
        default='PR',
    )

    class Meta:
        verbose_name = 'Зачисление на шаг'
        verbose_name_plural = 'Зачисления на шаги'
        ordering = ['pk']
        unique_together = ('step', 'user')
