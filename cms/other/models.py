from django.db import models
from PIL import Image
from users.models import CustomUser


class Category(models.Model):
    title = models.CharField(
        verbose_name='Название категории',
        max_length=25,
        unique=True,
        error_messages={
            "unique": "Такая категория уже существует",
        },
    )
    slug = models.SlugField(
        verbose_name='Slug категории',
        max_length=25,
        unique=True,
        error_messages={
            "unique": "Такой URL уже существует",
        },
    )
    icon = models.ImageField(
        verbose_name='Иконка категории',
        upload_to='icon/category/',
    )
    description = models.TextField(
        verbose_name='Описание категории',
        max_length=150,
    )
    author = models.ForeignKey(
        CustomUser,
        verbose_name='Автор категории',
        related_name='categories',
        on_delete=models.CASCADE,
        null=True,
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['pk']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        image = Image.open(self.icon.path)
        if image.width != 500 or image.height != 500:
            image = image.resize((500, 500), Image.ANTIALIAS)
            image.save(self.icon.path)


class Tag(models.Model):
    title = models.CharField(
        max_length=25,
        verbose_name='Название тега',
        unique=True,
        error_messages={
            "unique": "Такая тег уже существует",
        },
    )
    slug = models.SlugField(
        max_length=25,
        verbose_name='Slug',
        unique=True,
        error_messages={
            "unique": "Такой URL уже существует",
        },
    )
    icon = models.ImageField(
        upload_to='icon/tag/',
        verbose_name='Иконка тега',
    )
    description = models.TextField(
        max_length=150,
        verbose_name='Описание тега',
    )
    author = models.ForeignKey(
        CustomUser,
        verbose_name='Автор тега',
        related_name='tags',
        on_delete=models.CASCADE,
        null=True,
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['pk']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        image = Image.open(self.icon.path)
        if image.width != 500 or image.height != 500:
            image = image.resize((500, 500), Image.ANTIALIAS)
            image.save(self.icon.path)
