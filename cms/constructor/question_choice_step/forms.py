from django import forms
from lms.steps.models import QuestionChoiceStep
from cms.constructor.steps.forms import StepCreateForm


class QuestionChoiceStepCreateForm(StepCreateForm):
    class Meta(StepCreateForm.Meta):
        model = QuestionChoiceStep
        fields = StepCreateForm.Meta.fields + ['num_attempts']
        widgets = StepCreateForm.Meta.widgets | {
            'num_attempts': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Количество попыток',
                }
            ),
        }