from django.urls import path
from lms.homeworks.views import LMS_UserHomeworkList, LMS_UserHomeworkDetail


urlpatterns = [
    path('homeworks/my', LMS_UserHomeworkList.as_view(), name='LMS_UserHomeworkList'),
    path('homeworks/<str:course_slug>/<int:pk>/', LMS_UserHomeworkDetail.as_view(), name='LMS_UserHomeworkDetail')
]
