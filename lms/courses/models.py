from PIL import Image
from django.db import models
from django.urls import reverse
from cms.other.models import Category, Tag
from users.models import CustomUser


class Course(models.Model):
    title = models.CharField(
        verbose_name='Название курса',
        max_length=50,
    )
    slug = models.SlugField(
        verbose_name='Slug',
        max_length=25,
        unique=True,
        error_messages={
            'unique': 'Курс с таким URL уже существует',
        },
    )
    icon = models.ImageField(
        verbose_name='Иконка курса',
        upload_to='icon/course/',
    )
    description = models.TextField(
        verbose_name='Описание курса',
        max_length=150,
    )
    full_description = models.TextField(
        verbose_name='Полное описание курса',
    )
    is_published = models.BooleanField(
        verbose_name='Опубликовать?',
        default=False,
    )
    is_search = models.BooleanField(
        verbose_name='На главную страницу?',
        default=False,
    )
    date_create = models.DateTimeField(
        auto_now_add=True,
    )
    date_update = models.DateTimeField(
        auto_now=True,
    )
    price = models.PositiveIntegerField(
        default=0,
        verbose_name='Цена',
    )
    LEVEL_CHOICES = [
        ('AN', 'Любой'),
        ('BG', 'Начинающий'),
        ('MD', 'Средний'),
        ('SN', 'Эксперт'),
    ]
    course_level = models.CharField(
        verbose_name='Уровень курса',
        max_length=2,
        choices=LEVEL_CHOICES,
        default='AN',
    )
    category = models.ForeignKey(
        Category,
        related_name='courses',
        verbose_name='Категория',
        on_delete=models.CASCADE,
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='courses',
        verbose_name='Теги',
    )
    authors = models.ManyToManyField(
        CustomUser,
        related_name='courses',
        verbose_name='Автор курса',
    )
    rating = models.FloatField(
        verbose_name='Рейтинг курса',
        default=0,
    )
    min_age_students = models.PositiveIntegerField(
        verbose_name='Минимальный класс',
        default=0,
    )
    max_age_students = models.PositiveIntegerField(
        verbose_name='Максимальный класс',
        default=11,
    )
    video_url = models.URLField(
        verbose_name='Ссылка на видео',
        max_length=200,
        blank=True,
    )

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = '1. Курсы'
        ordering = ['pk']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        image = Image.open(self.icon.path)
        if image.width != 500 or image.height != 500:
            image = image.resize((500, 500), Image.ANTIALIAS)
            image.save(self.icon.path)

    def get_cms_detail_url(self):  # Проверить, обновить
        return reverse(
            'CMS_CourseDetail',
            kwargs={
                'course_slug': self.slug,
            },
        )

    def get_cms_update_url(self):
        return reverse(
            'CMS_CourseUpdate',
            kwargs={
                'course_slug': self.slug,
            },
        )

    def get_cms_delete_url(self):  # Проверить, обновить
        return reverse(
            'CMS_CourseDelete',
            kwargs={
                'course_slug': self.slug,
            },
        )

    def get_cms_create_topic_url(self):
        return reverse(
            'CMS_TopicCreate',
            kwargs={
                'course_slug': self.slug,
            },
        )

    def get_lms_detail_url(self):
        return reverse(
            'LMS_CourseDetail',
            kwargs={
                'course_slug': self.slug,
            },
        )

    def get_cms_topics_sort_url(self):
        return reverse(
            'CMS_TopicsSort',
            kwargs={
                'course_slug': self.slug,
            },
        )

    def get_cms_stat_url(self):
        return reverse(
            'CMS_CourseStatistics',
            kwargs={
                'course_slug': self.slug,
            },
        )

    def get_cms_submissions_url(self):
        return reverse(
            'CMS_CourseSubmissions',
            kwargs={
                'course_slug': self.slug,
            },
        )

    def get_steps_cnt(self):
        cnt = 0
        for topic in self.topics.all():
            cnt += topic.get_steps_cnt()

        return cnt

    def get_user_end_steps(self):

        cnt = 0

        for topic in self.topics.all():
            cnt += topic.get_user_end_steps()

        return cnt

    def get_user_percentage(self):
        if self.get_steps_cnt() == 0:
            return 0

        return int(self.get_user_end_steps() / self.get_steps_cnt() * 100)


class CourseEnroll(models.Model):
    course = models.ForeignKey(
        Course,
        related_name='courses_enrolls',
        verbose_name='Курс',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        CustomUser,
        related_name='courses_enrolls',
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
    )
    date_create = models.DateTimeField(
        auto_now=True,
    )
    date_update = models.DateTimeField(
        auto_now=True,
    )
    STATUS_CHOICES = [
        ('PR', 'Курс изучается'),
        ('OK', 'Курс изучен'),
    ]
    status = models.CharField(
        verbose_name='Статус',
        max_length=2,
        choices=STATUS_CHOICES,
        default='PR',
    )

    class Meta:
        verbose_name = 'Зачисление на курс'
        verbose_name_plural = '2. Зачисления на курсы'
        ordering = ['pk']
        unique_together = ('course', 'user')

    def __str__(self) -> str:
        return f'Зачисление на курс № {self.pk}'
