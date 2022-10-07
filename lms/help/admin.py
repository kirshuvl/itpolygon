from django.contrib import admin
from lms.help.models import ProjectExample, Skill


class ProjectExampleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'course')
    list_display_links = ('id', 'title', 'course')
    search_fields = ('id', 'title', 'course')


class SkillAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('id', 'title')


admin.site.register(ProjectExample, ProjectExampleAdmin)
admin.site.register(Skill, SkillAdmin)
