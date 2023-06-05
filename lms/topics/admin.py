from django.contrib import admin
from lms.topics.models import Topic


class TopicAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'is_published', 'number', 'course', 'author')
    list_display_links = ('id', 'title', 'slug', 'is_published', 'number', 'course', 'author')
    search_fields = ('id', 'title', 'slug', 'is_published', 'number', 'course', 'author')

admin.site.register(Topic, TopicAdmin)
