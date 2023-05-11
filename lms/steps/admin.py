from atexit import register
from django.contrib import admin
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelFilter, PolymorphicChildModelAdmin
from lms.steps.models import QuestionChoiceStep, Step, TestForQuestionChoiceStep, TextStep, UserAnswerForQuestionChoiceStep, VideoStep, QuestionStep, UserAnswerForQuestionStep, StepEnroll
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from lms.problems.models import ProblemStep
from lms.assignment.models import AssignmentStep
from lms.steps.models import *
class TextStepAdminForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = TextStep
        fields = '__all__'


class StepAdmin(PolymorphicParentModelAdmin):
    base_model = Step
    child_models = (TextStep, VideoStep, QuestionStep, QuestionChoiceStep, AssignmentStep, ProblemStep)
    list_filter = (PolymorphicChildModelFilter,)
    list_display = ('id', 'title', 'slug', 'is_published', 'points')
    list_display_links = ('id', 'title', 'slug', 'is_published', 'points')
    search_fields = ('id', 'title', 'slug', 'is_published', 'points')


class TextStepAdmin(PolymorphicChildModelAdmin):
    form = TextStepAdminForm
    base_model = TextStep
    list_display = ('id', 'title', 'slug', 'is_published', 'lesson', 'points')
    list_display_links = ('id', 'title', 'slug',
                          'is_published', 'lesson', 'points')
    search_fields = ('id', 'title', 'slug', 'is_published', 'lesson', 'points')


class VideoStepAdmin(PolymorphicChildModelAdmin):
    base_model = VideoStep
    list_display = ('id', 'title', 'slug', 'is_published', 'points')
    list_display_links = ('id', 'title', 'slug', 'is_published', 'points')
    search_fields = ('id', 'title', 'slug', 'is_published', 'points')


class QuestionStepAdmin(PolymorphicChildModelAdmin):
    base_model = QuestionStep
    list_display = ('id', 'title', 'slug', 'is_published', 'points')
    list_display_links = ('id', 'title', 'slug', 'is_published', 'points')
    search_fields = ('id', 'title', 'slug', 'is_published', 'points')


class UserAnswerForQuestionStepAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'is_correct', 'question')
    list_display_links = ('id', 'user', 'is_correct', 'question')
    search_fields = ('id', 'user', 'is_correct', 'question')


class QuestionChoiceStepAdmin(PolymorphicChildModelAdmin):
    base_model = QuestionChoiceStep
    list_display = ('id', 'title', 'slug', 'is_published', 'points')
    list_display_links = ('id', 'title', 'slug', 'is_published', 'points')
    search_fields = ('id', 'title', 'slug', 'is_published', 'points')


class TestForQuestionChoiceStepAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_correct', 'question')
    list_display_links = ('id', 'title', 'is_correct', 'question')
    search_fields = ('id', 'title', 'is_correct', 'question')


class UserAnswerForQuestionChoiceStepAdmin(admin.ModelAdmin):
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
admin.site.register(QuestionChoiceStep, QuestionChoiceStepAdmin)
admin.site.register(TestForQuestionChoiceStep, TestForQuestionChoiceStepAdmin)
admin.site.register(UserAnswerForQuestionChoiceStep, UserAnswerForQuestionChoiceStepAdmin)
admin.site.register(StepEnroll, StepEndrollAdmin)
