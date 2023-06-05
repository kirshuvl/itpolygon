from django import forms
from lms.steps.models import QuestionStep
from cms.constructor.steps.forms import StepCreateForm


class QuestionStepCreateForm(StepCreateForm):
    class Meta(StepCreateForm.Meta):
        model = QuestionStep
        fields = StepCreateForm.Meta.fields + ['answer', 'num_attempts']
        widgets = StepCreateForm.Meta.widgets | {
            'answer': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Правильный ответ',
                }
            ),
            'num_attempts': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Количество попыток',
                }
            ),
        }