from django.db import models
from polymorphic.models import PolymorphicModel
from users.models import CustomUser
from lms.lessons.models import Lesson
from django.urls import reverse


class Step(PolymorphicModel):
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

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Шаг урока'
        verbose_name_plural = 'Шаги уроков'
        ordering = ['title']

    def end_step(self):
        return reverse(
            'UserEndStep',
            kwargs={
                'course_slug': self.lesson.topic.course.slug,
                'topic_slug': self.lesson.topic.slug,
                'lesson_slug': self.lesson.slug,
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


class TextStep(Step):
    text = models.TextField(
        verbose_name='Текст'
    )

    class Meta:
        verbose_name = 'Текстовый шаг'
        verbose_name_plural = 'Текстовые шаги'
        ordering = ['pk']

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

    def step_icon_class(self):
        return 'bi-card-text'

    def type(self):
        return 'text'


class VideoStep(Step):
    video_url = models.URLField(
        verbose_name='Ссылка на видео',
        max_length=500,
    )

    class Meta:
        verbose_name = 'Видео шаг'
        verbose_name_plural = 'Видео шаги'
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

    def step_icon_class(self):
        return 'bi-play-btn'

    def type(self):
        return 'video'


class QuestionStep(Step):
    answer = models.CharField(
        verbose_name='Правильный ответ',
        max_length=250,
    )
    num_attempts = models.IntegerField(
        verbose_name='Количество попыток',
        default=-1,
    )

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
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

    def step_icon_class(self):
        return 'bi-question-square'

    def type(self):
        return 'question'


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
        return reverse(
            'QuestionStepDetail',
            kwargs={
                'course_slug': self.question.lesson.topic.course.slug,
                'topic_slug': self.question.lesson.topic.slug,
                'lesson_slug': self.question.lesson.slug,
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

    def step_icon_class(self):
        return 'bi-question-square'

    def type(self):
        return 'question'


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
