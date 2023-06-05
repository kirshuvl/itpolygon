from django.urls import path
from cms.constructor.courses.views import *

urlpatterns = [
    path('courses/my', CMS_CoursesList.as_view(), name='CMS_CoursesList'),
    path('courses/create/', CMS_CourseCreate.as_view(), name='CMS_CourseCreate'),
    path('courses/<str:course_slug>/detail', CMS_CourseDetail.as_view(), name='CMS_CourseDetail'),
    path('courses/<str:course_slug>/update', CMS_CourseUpdate.as_view(), name='CMS_CourseUpdate'),
    path('courses/<str:course_slug>/delete', CMS_CourseDelete.as_view(), name='CMS_CourseDelete'),
]