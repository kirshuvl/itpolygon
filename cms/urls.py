from django.urls import path, include

urlpatterns = [
    path('',
         include('cms.other.urls')
         ),
]
