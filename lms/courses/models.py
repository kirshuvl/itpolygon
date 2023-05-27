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
    is_outside = models.BooleanField(
        verbose_name='Опубликовать на главную страницу?',
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
        verbose_name_plural = 'Курсы'
        ordering = ['pk']
        db_table = 'course'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        image = Image.open(self.icon.path)
        if image.width != 500 or image.height != 500:
            image = image.resize((500, 500), Image.ANTIALIAS)
            image.save(self.icon.path)

    def get_lms_url(self):  # Проверить, обновить
        return reverse(
            'LMS_CourseDetail',
            kwargs={
                'course_slug': self.slug,
            },
        )

    def get_cms_url(self):  # Проверить, обновить
        return reverse(
            'CMS_CourseDetail',
            kwargs={
                'course_slug': self.slug,
            },
        )

    '''

    def get_stat_url(self): # Проверить, обновить
        return reverse(
            'CMS_CourseStatistics',
            kwargs={
                'course_slug': self.slug,
            },
        )

    def set_is_published(self): # Проверить, обновить
        return reverse(
            'course_check_publish',
            kwargs={
                'course_slug': self.slug,
            },
        )

    def create_topic(self): # Проверить, обновить
        return reverse(
            'CMS_TopicCreate',
            kwargs={
                'course_slug': self.slug,
            },
        )

    def get_update_url(self): # Проверить, обновить
        return reverse(
            'CMS_CourseUpdate',
            kwargs={
                'course_slug': self.slug,
            },
        )

    def get_delete_url(self): # Проверить, обновить
        return reverse(
            'CMS_CourseDelete',
            kwargs={
                'course_slug': self.slug,
            },
        )'''


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
        verbose_name_plural = 'Зачисления на курсы'
        ordering = ['pk']
        unique_together = ('course', 'user')
