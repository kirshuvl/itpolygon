from django.contrib import admin
from lms.problems.models import ProblemStep, TestUserAnswer, UserAnswerForProblemStep, TestForProblemStep


class ProblemStepAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'is_published', 'points')
    list_display_links = ('id', 'title', 'slug', 'is_published', 'points')
    search_fields = ('id', 'title', 'slug', 'is_published', 'points')


class TestForProblemStepAdmin(admin.ModelAdmin):
    list_display = ('id', 'problem', 'number', 'input', 'output')
    list_display_links = ('id', 'problem', 'number', 'input', 'output')
    search_fields = ('id', 'problem', 'number', 'input', 'output')


class UserAnswerForProblemStepAdmin(admin.ModelAdmin):
    list_display = ('id', 'user',)
    list_display_links = ('id', 'user',)
    search_fields = ('id', 'user',)


class TestUserAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'verdict')
    list_display_links = ('id', 'user', 'verdict')
    search_fields = ('id', 'user', 'verdict')


admin.site.register(ProblemStep, ProblemStepAdmin)
admin.site.register(TestForProblemStep, TestForProblemStepAdmin)
admin.site.register(UserAnswerForProblemStep, UserAnswerForProblemStepAdmin)
admin.site.register(TestUserAnswer, TestUserAnswerAdmin)
