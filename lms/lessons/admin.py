from django.contrib import admin
from lms.lessons.models import Lesson, LessonEnroll


class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'is_published')
    list_display_links = ('id', 'title', 'slug', 'is_published')
    search_fields = ('id', 'title', 'slug', 'is_published')


class LessonEnrollAdmin(admin.ModelAdmin):
    list_display = ('id', 'lesson', 'user', 'date_create', 'status')
    list_display_links = ('id', 'lesson', 'user', 'date_create', 'status')
    search_fields = ('id', 'lesson', 'user', 'date_create', 'status')


admin.site.register(Lesson, LessonAdmin)
admin.site.register(LessonEnroll, LessonEnrollAdmin)
