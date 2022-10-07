from django.db import models
from lms.courses.models import Course


class ProjectExample(models.Model):
    title = models.CharField(
            verbose_name='Название проекта',
            max_length=50,
    )
    slug = models.SlugField(
            verbose_name='Slug проекта',
            max_length=25,
            unique=True,
            error_messages={
                'unique': 'Проект с таким URL уже существует'
            },
    )
    icon = models.ImageField(
            verbose_name='Картинка проекта',
            upload_to='icon/project/',
            blank=True,
    )
    description = models.TextField(
            verbose_name='Описание проекта',
            max_length=1000,
    )
    video = models.FileField(
            verbose_name='Видео проекта',
            upload_to='icon/project/',
            blank=True,
    )
    use_video = models.BooleanField(
            verbose_name='Использовать видео?',
            default=False,
    )
    course = models.ForeignKey(
            Course,
            related_name='projects',
            verbose_name='Проект',
            on_delete=models.PROTECT,
    )

    class Meta:
        verbose_name = 'Проект для курса'
        verbose_name_plural = 'Проекты для курсов'
        ordering = ['pk']

    def __str__(self):
        return self.title


class Skill(models.Model):
    title = models.CharField(
            verbose_name='Название навыка',
            max_length=50,
    )
    slug = models.SlugField(
            verbose_name='Slug',
            max_length=25,
            unique=True,
            error_messages={
                'unique': 'Навык с таким URL уже существует'
            },
    )
    icon = models.ImageField(
            verbose_name='Картинка навыка',
            upload_to='icon/skill/',
    )
    description = models.TextField(
            verbose_name='Описание навыка',
            max_length=1000,
    )
    TYPE_CHOICES = [
        ('AN', 'AllSkills'),
        ('HS', 'HardSkills'),
        ('SS', 'SoftSkills'),
    ]
    type = models.CharField(
            verbose_name='Тип навыка',
            max_length=2,
            choices=TYPE_CHOICES,
            default='HS',
    )
    course = models.ManyToManyField(
            Course,
            verbose_name='Курсы',
            related_name='skills',
    )

    class Meta:
        verbose_name = 'Навыки для курса'
        verbose_name_plural = 'Навыки для курсов'
        ordering = ['pk']

    def __str__(self):
        return self.title
