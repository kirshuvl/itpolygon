from django.urls import path, include

urlpatterns = [
    path('cms/', include('cms.constructor.urls')),
    path('cms/', include('cms.other.urls')),
]
