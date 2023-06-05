from django import forms
from cms.constructor.forms import MixinForm
from lms.lessons.models import Lesson


class LessonCreateForm(MixinForm):
    class Meta:
        model = Lesson
        fields = ['title',
                  'slug',
                  'description',
                  'is_published',
                  'type',
                  ]
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Заголовок урока',
                }
            ),
            'slug': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Slug урока',
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': '5',
                    'placeholder': 'Краткое описание урока'
                }
            ),
            'is_published': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                    'placeholder': 'Опубликовать',
                    'role': 'switch',
                    'checked': True,
                }
            ),
            'type': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),
        }
