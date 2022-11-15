from django.contrib import admin
from lms.assignment.models import AssignmentStep, UserAnswerForAssignmentStep


class AssignmentStepAdmin(admin.ModelAdmin):
    base_model = AssignmentStep
    list_display = ('id', 'title', 'slug', 'is_published', 'lesson', 'points')
    list_display_links = ('id', 'title', 'slug',
                          'is_published', 'lesson', 'points')
    search_fields = ('id', 'title', 'slug', 'is_published', 'lesson', 'points')


class UserAnswerForAssignmentStepAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'is_correct', 'assignment')
    list_display_links = ('id', 'user', 'is_correct', 'assignment')
    search_fields = ('id', 'user', 'is_correct', 'assignment')


admin.site.register(AssignmentStep, AssignmentStepAdmin)
admin.site.register(UserAnswerForAssignmentStep,
                    UserAnswerForAssignmentStepAdmin)
