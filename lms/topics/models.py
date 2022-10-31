from django.db import models
from lms.courses.models import Course
from users.models import CustomUser


class Topic(models.Model):
    title = models.CharField(
        verbose_name='Название темы',
        max_length=50,
    )
    slug = models.SlugField(
        verbose_name='Slug',
        max_length=25,
        unique=True,
    )
    description = models.TextField(
        verbose_name='Описание темы',
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
        verbose_name='№ темы в курсе',
        default=1000,
    )
    course = models.ForeignKey(
        Course,
        related_name='topics',
        verbose_name='Курс',
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        CustomUser,
        related_name='topics',
        verbose_name='Автор темы',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'
        ordering = ['pk']

    def __str__(self):
        return self.title
