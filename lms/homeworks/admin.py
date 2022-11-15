from django.contrib import admin
from lms.homeworks.models import Homework


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


admin.site.register(Homework, HomeworkAdmin)