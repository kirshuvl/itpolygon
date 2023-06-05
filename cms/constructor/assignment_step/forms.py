from django import forms
from lms.assignment.models import AssignmentStep
from cms.constructor.steps.forms import StepCreateForm


class AssignmentStepCreateForm(StepCreateForm):
    class Meta(StepCreateForm.Meta):
        model = AssignmentStep
        fields = StepCreateForm.Meta.fields + ['file']
        widgets = StepCreateForm.Meta.widgets | {
            'file': forms.FileInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Файл'
                }
            ),
        }
