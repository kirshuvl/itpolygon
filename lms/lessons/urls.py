from django.urls import path
from lms.lessons.views import LMS_LessonDetail

urlpatterns = [
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/', LMS_LessonDetail.as_view(), name='LMS_LessonDetail'),
]
