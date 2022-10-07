from django.urls import path
from cms.other.views import CMSDashboard

urlpatterns = [
    path('', CMSDashboard.as_view(), name='CMSDashboard'),
]
