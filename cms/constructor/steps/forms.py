from django import forms
from cms.constructor.forms import MixinForm
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from lms.steps.models import Step


class StepCreateForm(MixinForm):
    class Meta:
        model = Step
        fields = ['title',
                  'slug',
                  'description',
                  'is_published',
                  'points',
                  ]
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Заголовок шага',
                }
            ),
            'slug': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Slug шага',
                }
            ),
            'description': CKEditorUploadingWidget(),
            'is_published': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                    'placeholder': 'Опубликовать',
                    'role': 'switch',
                }
            ),
            'points': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Баллы за шаг',
                }
            ),
        }
