from django.contrib import admin
from lms.homeworks.models import Homework, HomeworkStepConnection


class HomeworkAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'user',
                    'date_to',
                    )
    list_display_links = ('id',
                          'user',
                          'date_to',
                          )
    search_fields = ('id',
                     'user',
                     'date_to',
                     )


class HomeworkStepConnectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'homework', 'step', 'is_published')
    list_display_links = ('id', 'homework', 'step', 'is_published')
    search_fields = ('id', 'homework', 'step', 'is_published')


admin.site.register(Homework, HomeworkAdmin)
admin.site.register(HomeworkStepConnection, HomeworkStepConnectionAdmin)
