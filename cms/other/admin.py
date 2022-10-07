from django.contrib import admin
from cms.other.models import Category, Tag


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'title',
                    'slug'
                    )
    list_display_links = ('id',
                          'title',
                          'slug'
                          )
    search_fields = ('id',
                     'title',
                     'slug'
                     )


class TagAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'title',
                    'slug'
                    )
    list_display_links = ('id',
                          'title',
                          'slug'
                          )
    search_fields = ('id',
                     'title',
                     'slug'
                     )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
