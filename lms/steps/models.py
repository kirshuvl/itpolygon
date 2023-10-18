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
        return super().get_queryset().select_related('step_ptr')

    # .select_related('step_ptr__step__textstep', 'step_ptr__videostep', 'step_ptr__questionstep', 'step_ptr__questionchoicestep', 'step_ptr__assignmentstep', 'step_ptr__problemstep')


class VideoStepMixin():
    def video_url(self):
        if hasattr(self, 'videostep'):
            return self.videostep.video_url
        return None


class QuestionStepMixin():
    pass


class ProblemStepMixin:
    def get_problem(self):
        if hasattr(self, 'problemstep'):
            return self.problemstep
        return None

    def get_input_format(self):
        if hasattr(self, 'problemstep'):
            return self.problemstep.input_format
        return None

    def get_output_format(self):
        if hasattr(self, 'problemstep'):
            return self.problemstep.output_format
        return None

    def get_notes(self):
        if hasattr(self, 'problemstep'):
            return self.problemstep.notes
        return None

    def get_first_sample(self):
        if hasattr(self, 'problemstep'):
            return self.problemstep.first_sample
        return None

    def get_last_sample(self):
        if hasattr(self, 'problemstep'):
            return self.problemstep.last_sample
        return None

    def get_first_test(self):
        if hasattr(self, 'problemstep'):
            return self.problemstep.first_test
        return None

    def get_cputime(self):
        if hasattr(self, 'problemstep'):
            return self.problemstep.cputime
        return None

    def get_memory(self):
        if hasattr(self, 'problemstep'):
            return self.problemstep.memory
        return None


class AssignmentStepMixin():
    def get_file(self):
        if hasattr(self, 'assignmentstep'):
            return self.assignmentstep.file
        return None

    def get_file_name(self):
        if hasattr(self, 'assignmentstep'):
            return self.assignmentstep.file.name.split('/')[-1].split('.')[0]
        return None

    def get_file_format(self):
        if hasattr(self, 'assignmentstep'):
            return self.assignmentstep.file.name.split('/')[-1].split('.')[-1]
        return None


class StepsMixin(VideoStepMixin, QuestionStepMixin, ProblemStepMixin, AssignmentStepMixin):
    def get_num_attempts(self):
        return self.connections.first().num_attempts


class FrontMixin():
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


class Step(models.Model, StepsMixin, FrontMixin):
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
    objects = StepManager()

    class Meta:
        verbose_name = 'Шаг урока'
        verbose_name_plural = 'Шаги уроков'
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_cms_update_url(self):
        lesson: Lesson = self.connections.first().lesson
        if hasattr(self, 'textstep'):
            url = 'CMS_TextStepUpdate'
        elif hasattr(self, 'videostep'):
            url = 'CMS_VideoStepUpdate'
        elif hasattr(self, 'questionstep'):
            url = 'CMS_QuestionStepUpdate'
        elif hasattr(self, 'questionchoicestep'):
            url = 'CMS_QuestionChoiceStepUpdate'
        elif hasattr(self, 'problemstep'):
            url = 'CMS_ProblemStepUpdate'
        elif hasattr(self, 'assignmentstep'):
            url = 'CMS_AssignmentStepUpdate'
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

    def get_cms_detail_url(self):
        lesson: Lesson = self.connections.first().lesson
        if hasattr(self, 'textstep'):
            url = 'CMS_TextStepDetail'
        elif hasattr(self, 'videostep'):
            url = 'CMS_VideoStepDetail'
        elif hasattr(self, 'questionstep'):
            url = 'CMS_QuestionStepDetail'
        elif hasattr(self, 'questionchoicestep'):
            url = 'CMS_QuestionChoiceStepDetail'
        elif hasattr(self, 'problemstep'):
            url = 'CMS_ProblemStepDetail'
        elif hasattr(self, 'assignmentstep'):
            url = 'CMS_AssignmentStepDetail'
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

    def get_cms_delete_url(self):
        lesson: Lesson = self.connections.first().lesson
        return reverse(
            'CMS_StepDelete',
            kwargs={
                'course_slug': lesson.topic.course.slug,
                'topic_slug': lesson.topic.slug,
                'lesson_slug': lesson.slug,
                'step_slug': self.slug,
            },
        )

    def get_connect(self):
        connect = self.connections.first()
        return connect

    # OLD

    def get_lms_detail_url(self):
        lesson: Lesson = self.connections.first().lesson
        if hasattr(self, 'textstep'):
            url = 'LMS_TextStepDetail'
        elif hasattr(self, 'videostep'):
            url = 'LMS_VideoStepDetail'
        elif hasattr(self, 'questionstep'):
            url = 'LMS_QuestionStepDetail'
        elif hasattr(self, 'questionchoicestep'):
            url = 'LMS_QuestionChoiceStepDetail'
        elif hasattr(self, 'problemstep'):
            url = 'LMS_ProblemStepDetail'
        elif hasattr(self, 'assignmentstep'):
            url = 'LMS_AssignmentStepDetail'
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
        related_name='connections',
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
    objects = LessonStepConnectionManager()

    class Meta:
        verbose_name = 'Шаг - Урок'
        verbose_name_plural = '0. Шаги - Уроки'
        ordering = ['lesson', 'step', 'number']
        unique_together = ('lesson', 'step', 'number')

    def get_cms_up_url(self):
        return reverse(
            'CMS_ConnectUp',
            kwargs={
                'course_slug': self.lesson.topic.course.slug,
                'topic_slug': self.lesson.topic.slug,
                'lesson_slug': self.lesson.slug,
                'step_slug': self.step.slug,
            },
        )

    def get_cms_down_url(self):

        return reverse(
            'CMS_ConnectDown',
            kwargs={
                'course_slug': self.lesson.topic.course.slug,
                'topic_slug': self.lesson.topic.slug,
                'lesson_slug': self.lesson.slug,
                'step_slug': self.step.slug,
            },
        )

    def get_cms_is_published_url(self):

        return reverse(
            'CMS_ConnectPublish',
            kwargs={
                'course_slug': self.lesson.topic.course.slug,
                'topic_slug': self.lesson.topic.slug,
                'lesson_slug': self.lesson.slug,
                'step_slug': self.step.slug,
            },
        )

    def get_cms_connect_delete_url(self):

        return reverse(
            'CMS_ConnectDelete',
            kwargs={
                'course_slug': self.lesson.topic.course.slug,
                'topic_slug': self.lesson.topic.slug,
                'lesson_slug': self.lesson.slug,
                'step_slug': self.step.slug,
            },
        )


class TextStep(Step):
    objects = DefaultStepManager()

    class Meta:
        verbose_name = 'Текстовый шаг'
        verbose_name_plural = '1. Текстовые шаги'
        ordering = ['pk']

    def get_cms_detail_url(self):
        lesson: Lesson = self.connections.first().lesson

        return reverse(
            'CMS_TextStepDetail',
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
            'CMS_TextStepUpdate',
            kwargs={
                'course_slug': lesson.topic.course.slug,
                'topic_slug': lesson.topic.slug,
                'lesson_slug': lesson.slug,
                'step_slug': self.slug,
            },
        )

    def get_cms_delete_url(self):
        lesson: Lesson = self.connections.first().lesson
        return reverse(
            'CMS_StepDelete',
            kwargs={
                'course_slug': lesson.topic.course.slug,
                'topic_slug': lesson.topic.slug,
                'lesson_slug': lesson.slug,
                'step_slug': self.slug,
            },
        )

    def icon_class(self):
        return 'bi-card-text'


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

    def get_cms_detail_url(self):
        lesson: Lesson = self.connections.first().lesson

        return reverse(
            'CMS_VideoStepDetail',
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
            'CMS_VideoStepUpdate',
            kwargs={
                'course_slug': lesson.topic.course.slug,
                'topic_slug': lesson.topic.slug,
                'lesson_slug': lesson.slug,
                'step_slug': self.slug,
            },
        )

    def icon_class(self):
        return 'bi-play-btn'


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
        verbose_name = 'Вопрос с вводом ответа'
        verbose_name_plural = '3. Вопросы c вводом ответа'
        ordering = ['title']

    def get_cms_detail_url(self):
        lesson: Lesson = self.connections.first().lesson

        return reverse(
            'CMS_QuestionStepDetail',
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
            'CMS_QuestionStepUpdate',
            kwargs={
                'course_slug': lesson.topic.course.slug,
                'topic_slug': lesson.topic.slug,
                'lesson_slug': lesson.slug,
                'step_slug': self.slug,
            },
        )

    def icon_class(self):
        return 'bi-question-square'


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
        verbose_name_plural = '3.1 Ответы пользователей'
        ordering = ['pk']

    '''def get_absolute_url(self):
        lesson: Lesson = self.connections.first().lesson
        return reverse(
            'LMS_QuestionStepDetail',
            kwargs={
                'course_slug': lesson.topic.course.slug,
                'topic_slug': lesson.topic.slug,
                'lesson_slug': lesson.slug,
                'step_slug': self.question.slug,
            },
        )'''


class QuestionChoiceStep(Step):
    num_attempts = models.IntegerField(
        verbose_name='Количество попыток',
        default=-1,
    )
    objects = DefaultStepManager()

    class Meta:
        verbose_name = 'Вопрос с выбором ответа'
        verbose_name_plural = '4. Вопросы с выбором ответа'
        ordering = ['title']

    def get_cms_detail_url(self):
        lesson: Lesson = self.connections.first().lesson

        return reverse(
            'CMS_QuestionChoiceStepDetail',
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
            'CMS_QuestionChoiceStepUpdate',
            kwargs={
                'course_slug': lesson.topic.course.slug,
                'topic_slug': lesson.topic.slug,
                'lesson_slug': lesson.slug,
                'step_slug': self.slug,
            },
        )

    def icon_class(self):
        return 'bi-question-square'


class TestForQuestionChoiceStep(models.Model):
    answer = models.CharField(
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
        verbose_name_plural = '4.1 Варианты ответа'
        ordering = ['pk']

    def __str__(self) -> str:
        return self.answer


class UserAnswerForQuestionChoiceStep(models.Model):
    user_answer = models.ForeignKey(
        TestForQuestionChoiceStep,
        related_name='question_choice_answers',
        verbose_name='Ответ пользователя',
        on_delete=models.CASCADE,
    )
    is_correct = models.BooleanField(
        default=False,
    )
    user = models.ForeignKey(
        CustomUser,
        related_name='question_choice_answers',
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
    )
    question = models.ForeignKey(
        QuestionChoiceStep,
        related_name='question_choice_answers',
        verbose_name='Вопрос',
        on_delete=models.CASCADE,
    )
    date_create = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        verbose_name = 'Ответ пользователя'
        verbose_name_plural = '4.2 Ответы пользователей'
        ordering = ['pk']

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
