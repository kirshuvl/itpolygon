from django.db import models
from django.urls import reverse_lazy
from lms.courses.models import Course
from users.models import CustomUser


class Promocode(models.Model):
    title = models.CharField(
        verbose_name='Название промокода',
        max_length=30,
        unique=True,
    )
    date_create = models.DateTimeField(
        auto_now_add=True,
    )
    date_update = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'
        ordering = ['pk']

    def __str__(self):
        return self.title


class Status(models.Model):
    title = models.CharField(
        verbose_name='Заголовок статуса заявки',
        max_length=30,
    )

    class Meta:
        verbose_name = 'Заявки. Статус'
        verbose_name_plural = 'Заявки. Статусы'
        ordering = ['pk']

    def __str__(self):
        return self.title


class UserLead(models.Model):
    parent_first_name = models.CharField(
        verbose_name='Имя родителя',
        max_length=30,
    )
    parent_middle_name = models.CharField(
        verbose_name='Отчество родителя',
        max_length=30,
    )
    parent_last_name = models.CharField(
        verbose_name='Фамилия родителя',
        max_length=30,
    )
    child_first_name = models.CharField(
        verbose_name='Имя ребенка',
        max_length=30,
    )
    child_middle_name = models.CharField(
        verbose_name='Отчество ребенка',
        max_length=30,
    )
    child_last_name = models.CharField(
        verbose_name='Фамилия ребенка',
        max_length=30,
    )
    CLASS_CHOICES = [
        ('Default', 'Не выбрано'),
        ('1', '1 Класс'),
        ('2', '2 Класс'),
        ('3', '3 Класс'),
        ('4', '4 Класс'),
        ('5', '5 Класс'),
        ('6', '6 Класс'),
        ('7', '7 Класс'),
        ('8', '8 Класс'),
        ('9', '9 Класс'),
        ('10', '10 Класс'),
        ('11', '11 Класс'),
        ('Student', 'Студент'),

    ]
    child_class = models.CharField(
        verbose_name='Класс',
        max_length=10,
        choices=CLASS_CHOICES,
        default='Default',
    )
    phone = models.CharField(
        verbose_name='Номер телефона',
        max_length=11,
    )
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
    )
    course = models.ForeignKey(
        Course,
        verbose_name='Курс',
        related_name='userleads',
        on_delete=models.PROTECT,
    )
    promocode = models.ForeignKey(
        Promocode,
        related_name='userleads',
        verbose_name='Промокод',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    info = models.TextField(
        verbose_name='Информация',
    )
    date_create = models.DateTimeField(
        auto_now_add=True,
    )
    status = models.ForeignKey(
        Status,
        related_name='userleads',
        verbose_name='Статус',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Заявка. Запись на курс'
        verbose_name_plural = 'Заявки. Запись на курс'
        ordering = ['pk']

    def __str__(self):
        return self.parent_first_name

    def get_absolute_url(self):
        return reverse_lazy(
            'LeadDetail',
            kwargs={
                'lead_pk': self.pk,
            },
        )


class UserFeedBack(models.Model):
    parent_first_name = models.CharField(
        verbose_name='Имя родителя',
        max_length=30,
    )
    parent_middle_name = models.CharField(
        verbose_name='Отчество родителя',
        max_length=30,
        blank=True,
    )
    parent_last_name = models.CharField(
        verbose_name='Фамилия родителя',
        max_length=30,
    )
    phone = models.CharField(
        verbose_name='Номер телефона',
        max_length=11,
    )
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
    )
    date_create = models.DateTimeField(
        auto_now_add=True,
    )
    status = models.ForeignKey(
        Status,
        related_name='userfeedbacks',
        verbose_name='Статус',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Заявка. Обратная связь'
        verbose_name_plural = 'Заявки. Обратная связь'
        ordering = ['pk']

    def __str__(self):
        return self.parent_first_name


class LeadComment(models.Model):
    text = models.TextField(
        verbose_name='Комментарий',
    )
    lead = models.ForeignKey(
        UserLead,
        related_name='leadcomments',
        verbose_name='Лид',
        on_delete=models.CASCADE,
    )
    date_create = models.DateTimeField(
        auto_now_add=True,
    )
    date_update = models.DateTimeField(
        auto_now=True,
    )
    author = models.ForeignKey(
        CustomUser,
        related_name='leadcomments',
        verbose_name='Автор',
        on_delete=models.PROTECT,
    )
    status = models.ForeignKey(
        Status,
        related_name='leadcomments',
        verbose_name='Статус',
        on_delete=models.PROTECT,
    )

    class Meta:
        verbose_name = 'Заявка. Комментарий'
        verbose_name_plural = 'Заявки. Комментарии'
        ordering = ['pk']
