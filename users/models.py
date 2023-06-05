from PIL import Image
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from users.managers import CustomUserManager


class CustomUser(AbstractUser, PermissionsMixin):
    username = None
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=30
    )
    middle_name = models.CharField(
        verbose_name='Отчество',
        max_length=30,
        blank=True
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=30
    )
    nickname = models.CharField(
        verbose_name='Username',
        max_length=30,
        unique=True,
        error_messages={
            'unique': 'Пользователь с таким никнеймом уже зарегистрировался'
        }
    )
    phone = models.CharField(
        verbose_name='Номер телефона',
        max_length=11,
        unique=True,
        error_messages={
            'unique': 'Пользователь с таким номером уже зарегистрировался'
        }
    )
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        unique=True,
        error_messages={
            'unique': 'Пользователь с такой почтой уже зарегистрировался'
        }
    )
    STATUS_CHOICES = [
        ('TC', 'Учитель'),
        ('ST', 'Ученик'),
        ('PR', 'Родитель')
    ]
    status = models.CharField(
        verbose_name='Статус',
        max_length=2,
        choices=STATUS_CHOICES,
        default='ST',
        blank=True
    )
    school = models.CharField(
        verbose_name='Номер школы',
        max_length=30,
        null=True
    )
    date_create = models.DateTimeField(
        auto_now_add=True
    )
    coin = models.PositiveIntegerField(
        verbose_name='Монеты',
        default=0
    )
    icon = models.ImageField(
        verbose_name='Фотография профиля',
        upload_to='icon/user/',
        null=True,
        default='main/default_user_image.png')
    bio = models.TextField(
        verbose_name='Биография',
        default='Биография сгенерирована роботом. Напишите тут ее самостоятельно :)',
        max_length=2000,
        blank=True
    )
    parent = models.ManyToManyField(
        'self',
        verbose_name='Родитель',
        blank=True
    )
    is_active = models.BooleanField(
        verbose_name='Активен',
        default=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['pk']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        image = Image.open(self.icon.path)
        if image.width != 500 or image.height != 500:
            image = image.resize((500, 500), Image.ANTIALIAS)
            image.save(self.icon.path)
