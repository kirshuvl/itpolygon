from django.contrib import admin
from lms.lessons.models import Lesson


class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'is_published', 'number', 'topic', 'author')
    list_display_links = ('id', 'title', 'slug', 'is_published', 'number', 'topic', 'author')
    search_fields = ('id', 'title', 'slug', 'is_published', 'number', 'topic', 'author')


admin.site.register(Lesson, LessonAdmin)
