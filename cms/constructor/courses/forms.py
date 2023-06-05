from django import forms
from lms.courses.models import Course
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from cms.constructor.forms import MixinForm


class CourseCreateForm(MixinForm):
    class Meta:
        model = Course
        fields = ['title',
                  'slug',
                  'icon',
                  'description',
                  'full_description',
                  'is_published',
                  'is_search',
                  'price',
                  'course_level',
                  'category',
                  'tags',
                  'min_age_students',
                  'max_age_students',
                  'video_url',
                  ]
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Название курса',
                }
            ),
            'slug': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Slug курса',
                }
            ),
            'icon': forms.FileInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Иконка курса'
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': '5',
                    'placeholder': 'Описание курса'
                }
            ),
            'full_description': CKEditorUploadingWidget(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Опубликовать'
                }
            ),
            'is_published': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                    'placeholder': 'Опубликовать',
                    'role': 'switch'
                }
            ),
            'is_search': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                    'placeholder': 'Поместить на главную?',
                    'role': 'switch'
                }
            ),
            'price': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Цена курса',
                    'type': 'number',
                    'step': '1'
                }
            ),
            'course_level': forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Уровень курса',
                },
            ),
            'category': forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Уровень курса',
                },
            ),
            'tags': forms.SelectMultiple(
                attrs={
                    'class': 'form-select',
                    'size': '3'
                },
            ),
            'min_age_students': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Минимальный класс',
                }
            ),
            'max_age_students': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Максимальный класс',
                }
            ),
            'video_url': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ссылка на видео',
                }
            ),
        }

    def clean_video_url(self):
        video_url = self.cleaned_data.get('video_url')

        return video_url
