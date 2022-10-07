from django.contrib import admin
from lms.topics.models import Topic, TopicEnroll


class TopicAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'is_published')
    list_display_links = ('id', 'title', 'slug', 'is_published')
    search_fields = ('id', 'title', 'slug', 'is_published')


class TopicEnrollAdmin(admin.ModelAdmin):
    list_display = ('id', 'topic', 'user', 'date_create', 'status')
    list_display_links = ('id', 'topic', 'user', 'date_create', 'status')
    search_fields = ('id', 'topic', 'user', 'date_create', 'status')


admin.site.register(Topic, TopicAdmin)
admin.site.register(TopicEnroll, TopicEnrollAdmin)
