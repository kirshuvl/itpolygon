from django.urls import path
from lms.courses.views import CoursesList, LMS_UserCoursesList, LMS_CourseDetail

urlpatterns = [
    path('courses/my/', LMS_UserCoursesList.as_view(), name='LMS_UserCoursesList'),
    path('courses/all/', CoursesList.as_view(), name='CoursesList'),
    path('courses/<str:course_slug>/', LMS_CourseDetail.as_view(), name='LMS_CourseDetail'),
]
