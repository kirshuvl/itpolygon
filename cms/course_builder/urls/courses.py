from django.urls import path
from cms.course_builder.views.courses import *

urlpatterns = [
    path('courses/my', CMS_CoursesList.as_view(), name='CMS_CoursesList'),
    path('courses/create/', CMS_CourseCreate.as_view(), name='CMS_CourseCreate'),
    path('courses/<str:course_slug>/', CMS_CourseDetail.as_view(), name='CMS_CourseDetail'),
    path('courses/<str:course_slug>/update', CMS_CourseUpdate.as_view(), name='CMS_CourseUpdate'),
    path('courses/<str:course_slug>/delete', CMS_CourseDelete.as_view(), name='CMS_CourseDelete'),
    path('course/<str:course_slug>/check_publish/', course_check_publish, name='course_check_publish'),
]