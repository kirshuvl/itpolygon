from django.contrib import admin
from crm.lead.models import Promocode, Status, UserLead, UserFeedBack, LeadComment


class PromocodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('id', 'title')


class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('id', 'title')


class UserLeadAdmin(admin.ModelAdmin):
    list_display = ('id', 'parent_first_name', 'parent_middle_name',
                    'parent_last_name', 'child_class', 'promocode', 'course',)
    list_display_links = ('id', 'parent_first_name', 'parent_middle_name', 'parent_last_name',
                          'child_class', 'promocode', 'course',)
    search_fields = ('id', 'parent_first_name', 'parent_middle_name',
                     'parent_last_name', 'child_class', 'promocode', 'course',)


class UserFeedBackAdmin(admin.ModelAdmin):
    list_display = ('id', 'parent_first_name',
                    'parent_middle_name', 'parent_last_name')
    list_display_links = ('id', 'parent_first_name',
                          'parent_middle_name', 'parent_last_name')
    search_fields = ('id', 'parent_first_name',
                     'parent_middle_name', 'parent_last_name')


class LeadCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'lead')
    list_display_links = ('id', 'lead')
    search_fields = ('id', 'lead')


admin.site.register(Promocode, PromocodeAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(UserLead, UserLeadAdmin)
admin.site.register(UserFeedBack, UserFeedBackAdmin)
admin.site.register(LeadComment, LeadCommentAdmin)
