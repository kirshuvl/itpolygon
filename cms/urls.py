from django.urls import path, include

urlpatterns = [
    path('', include('cms.feedback.urls')),
    path('cms/', include('cms.groups.urls')),
    path('cms/', include('cms.other.urls')),
]
