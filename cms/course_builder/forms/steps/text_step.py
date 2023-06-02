from django import forms
from cms.course_builder.forms.steps.steps import StepCreateForm
from lms.steps.models import TextStep
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class TextStepCreateForm(StepCreateForm):
    class Meta(StepCreateForm.Meta):
        model = TextStep
        fields = StepCreateForm.Meta.fields
        widgets = StepCreateForm.Meta.widgets
