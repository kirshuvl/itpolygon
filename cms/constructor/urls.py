from django.urls import path, include

urlpatterns = [
    path('', include('cms.constructor.courses.urls')),
    path('', include('cms.constructor.topics.urls')),
    path('', include('cms.constructor.lessons.urls')),
    path('', include('cms.constructor.steps.urls')),
]