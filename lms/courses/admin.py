from django.contrib import admin
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from lms.courses.models import Course, CourseEnroll


class CourseAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())
    full_description = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Course
        fields = '__all__'


class CourseAdmin(admin.ModelAdmin):
    form = CourseAdminForm
    list_display = ('id', 'title', 'slug', 'icon',  'is_published')
    list_display_links = ('id', 'title', 'slug', 'icon', 'is_published')
    search_fields = ('id', 'title', 'slug', 'icon', 'is_published')


class CourseEnrollAdmin(admin.ModelAdmin):
    list_display = ('id', 'course', 'user', 'date_create', 'status')
    list_display_links = ('id', 'course', 'user', 'date_create', 'status')
    search_fields = ('id', 'course', 'user', 'date_create', 'status')


admin.site.register(Course, CourseAdmin)
admin.site.register(CourseEnroll, CourseEnrollAdmin)
