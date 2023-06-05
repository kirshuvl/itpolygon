from django import forms
from cms.constructor.steps.forms import StepCreateForm
from lms.steps.models import TextStep
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from lms.steps.models import VideoStep


class VideoStepCreateForm(StepCreateForm):
    class Meta(StepCreateForm.Meta):
        model = VideoStep
        fields = StepCreateForm.Meta.fields + ['video_url']
        widgets = StepCreateForm.Meta.widgets | {
            'video_url': forms.URLInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ссылка на видео',
                }
            ),
        }
