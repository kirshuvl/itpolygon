from django.urls import path
from lms.lessons.views import LMS_LessonDetail, LessonStatistics

urlpatterns = [
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/', LMS_LessonDetail.as_view(), name='LMS_LessonDetail'),
    path('lessons/statistics/<str:lesson_slug>/', LessonStatistics.as_view(), name='LessonStatistics'),
]
