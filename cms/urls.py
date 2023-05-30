from django.urls import path, include

urlpatterns = [
    #path('', include('cms.feedback.urls')),
    #path('cms/', include('cms.groups.urls')),
    path('cms/', include('cms.other.urls')),
    path('cms/', include('cms.course_builder.urls.courses')),
    path('cms/', include('cms.course_builder.urls.topics')),
    path('cms/', include('cms.course_builder.urls.lessons')),
    path('cms/', include('cms.course_builder.urls.steps')),
]
