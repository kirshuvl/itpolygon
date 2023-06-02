from django.contrib import admin
from lms.assignment.models import AssignmentStep, ReviewForUserAnswerForAssignmentStep, UserAnswerForAssignmentStep
from polymorphic.admin import PolymorphicChildModelAdmin

class AssignmentStepAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'is_published', 'points')
    list_display_links = ('id', 'title', 'slug', 'is_published', 'points')
    search_fields = ('id', 'title', 'slug', 'is_published', 'points')


class UserAnswerForAssignmentStepAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'is_correct', 'assignment')
    list_display_links = ('id', 'user', 'is_correct', 'assignment')
    search_fields = ('id', 'user', 'is_correct', 'assignment')


class ReviewForUserAnswerForAssignmentStepAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'user_answer')
    list_display_links = ('id', 'user', 'user_answer')
    search_fields = ('id', 'user', 'user_answer')


admin.site.register(AssignmentStep, AssignmentStepAdmin)
admin.site.register(UserAnswerForAssignmentStep, UserAnswerForAssignmentStepAdmin)
admin.site.register(ReviewForUserAnswerForAssignmentStep, ReviewForUserAnswerForAssignmentStepAdmin)
