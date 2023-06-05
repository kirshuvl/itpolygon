from django import forms
from lms.topics.models import Topic
from cms.constructor.forms import MixinForm


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
