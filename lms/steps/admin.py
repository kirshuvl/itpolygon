from atexit import register
from django.contrib import admin
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelFilter, PolymorphicChildModelAdmin
from lms.steps.models import Step, TextStep, VideoStep, QuestionStep, UserAnswerForQuestionStep, StepEnroll
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

class TextStepAdminForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = TextStep
        fields = '__all__'

class StepAdmin(PolymorphicParentModelAdmin):
    base_model = Step
    child_models = (TextStep, VideoStep)
    list_filter = (PolymorphicChildModelFilter,)
    list_display = ('id', 'title', 'slug', 'is_published')
    list_display_links = ('id', 'title', 'slug', 'is_published')
    search_fields = ('id', 'title', 'slug', 'is_published')


class TextStepAdmin(PolymorphicChildModelAdmin):
    form = TextStepAdminForm
    base_model = TextStep
    list_display = ('id', 'title', 'slug', 'is_published', 'lesson')
    list_display_links = ('id', 'title', 'slug', 'is_published', 'lesson')
    search_fields = ('id', 'title', 'slug', 'is_published', 'lesson')


class VideoStepAdmin(PolymorphicChildModelAdmin):
    base_model = VideoStep
    list_display = ('id', 'title', 'slug', 'is_published')
    list_display_links = ('id', 'title', 'slug', 'is_published')
    search_fields = ('id', 'title', 'slug', 'is_published')


class QuestionStepAdmin(PolymorphicChildModelAdmin):
    base_model = QuestionStep
    list_display = ('id', 'title', 'slug', 'is_published')
    list_display_links = ('id', 'title', 'slug', 'is_published')
    search_fields = ('id', 'title', 'slug', 'is_published')


class UserAnswerForQuestionStepAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'is_correct', 'question')
    list_display_links = ('id', 'user', 'is_correct', 'question')
    search_fields = ('id', 'user', 'is_correct', 'question')


class StepEndrollAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'step', 'status')
    list_display_links = ('id', 'user', 'step', 'status')
    search_fields = ('id', 'user', 'step', 'status')


admin.site.register(Step, StepAdmin)
admin.site.register(TextStep, TextStepAdmin)
admin.site.register(VideoStep, VideoStepAdmin)
admin.site.register(QuestionStep, QuestionStepAdmin)
admin.site.register(UserAnswerForQuestionStep, UserAnswerForQuestionStepAdmin)
admin.site.register(StepEnroll, StepEndrollAdmin)
