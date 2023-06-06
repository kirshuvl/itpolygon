from django.db import models
from users.models import CustomUser
from lms.topics.models import Topic
from django.urls import reverse


class LessonManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('topic__course')


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

    objects = LessonManager()

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ['pk']

    def __str__(self):
        return self.title

    def get_cms_detail_url(self):
        return reverse(
            'CMS_LessonDetail',
            kwargs={
                'course_slug': self.topic.course.slug,
                'topic_slug': self.topic.slug,
                'lesson_slug': self.slug,
            }
        )

    def get_cms_update_url(self):
        return reverse(
            'CMS_LessonUpdate',
            kwargs={
                'course_slug': self.topic.course.slug,
                'topic_slug': self.topic.slug,
                'lesson_slug': self.slug,
            }
        )

    def get_cms_delete_url(self):
        return reverse(
            'CMS_LessonDelete',
            kwargs={
                'course_slug': self.topic.course.slug,
                'topic_slug': self.topic.slug,
                'lesson_slug': self.slug,
            },
        )

    # Создать шаги

    def get_cms_create_text_step_url(self):
        return reverse(
            'CMS_TextStepCreate',
            kwargs={
                'course_slug': self.topic.course.slug,
                'topic_slug': self.topic.slug,
                'lesson_slug': self.slug
            },
        )

    def get_cms_create_video_step_url(self):
        return reverse(
            'CMS_VideoStepCreate',
            kwargs={
                'course_slug': self.topic.course.slug,
                'topic_slug': self.topic.slug,
                'lesson_slug': self.slug
            },
        )

    def get_cms_create_question_step_url(self):
        return reverse(
            'CMS_QuestionStepCreate',
            kwargs={
                'course_slug': self.topic.course.slug,
                'topic_slug': self.topic.slug,
                'lesson_slug': self.slug
            },
        )

    def get_cms_create_question_choice_step_url(self):
        return reverse(
            'CMS_QuestionChoiceStepCreate',
            kwargs={
                'course_slug': self.topic.course.slug,
                'topic_slug': self.topic.slug,
                'lesson_slug': self.slug
            },
        )

    def get_cms_create_problem_step_url(self):
        return reverse(
            'CMS_ProblemStepCreate',
            kwargs={
                'course_slug': self.topic.course.slug,
                'topic_slug': self.topic.slug,
                'lesson_slug': self.slug
            },
        )

    def get_cms_create_assignment_step_url(self):
        return reverse(
            'CMS_AssignmentStepCreate',
            kwargs={
                'course_slug': self.topic.course.slug,
                'topic_slug': self.topic.slug,
                'lesson_slug': self.slug
            },
        )

    def get_cms_text_step_from_library_url(self):
        return reverse(
            'CMS_TextStepFromLibrary',
            kwargs={
                'course_slug': self.topic.course.slug,
                'topic_slug': self.topic.slug,
                'lesson_slug': self.slug,
            }
        )

    def get_lms_detail_url(self):
        return reverse(
            'LMS_LessonDetail',
            kwargs={
                'course_slug': self.topic.course.slug,
                'topic_slug': self.topic.slug,
                'lesson_slug': self.slug,
            },
        )

    def get_cms_up_url(self):
        return reverse(
            'CMS_LessonUp',
            kwargs={
                'course_slug': self.topic.course.slug,
                'topic_slug': self.topic.slug,
                'lesson_slug': self.slug,
            },
        )

    def get_cms_down_url(self):
        return reverse(
            'CMS_LessonDown',
            kwargs={
                'course_slug': self.topic.course.slug,
                'topic_slug': self.topic.slug,
                'lesson_slug': self.slug,
            },
        )

    def get_cms_is_published_url(self):
        return reverse(
            'CMS_LessonPublish',
            kwargs={
                'lesson_slug': self.slug,
            },
        )

    def get_cms_steps_sort_url(self):
        return reverse(
            'CMS_StepsSort',
            kwargs={
                'lesson_slug': self.slug,
            },
        )

    def get_steps_cnt(self):

        return self.connections.count()

    def get_user_end_steps(self):

        cnt = 0

        for connect in self.connections.all():
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
