from django import forms
from lms.courses.models import Course
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from cms.course_builder.forms.forms import MixinForm
from lms.topics.models import Topic


class TopicCreateForm(MixinForm):
    class Meta:
        model = Topic
        fields = ['title',
                  'slug',
                  'description',
                  'is_published',
                  ]
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Заголовок темы',
                }
            ),
            'slug': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Slug темы',
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': '5',
                    'placeholder': 'Краткое описание темы'
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
        }
