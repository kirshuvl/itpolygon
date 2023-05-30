from django.urls import path
from cms.course_builder.views.lessons import *


urlpatterns = [
    path('courses/<str:course_slug>/<str:topic_slug>/create', CMS_LessonCreate.as_view(), name='CMS_LessonCreate'),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/', CMS_LessonDetail.as_view(), name='CMS_LessonDetail'), 
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/update', CMS_LessonUpdate.as_view(), name='CMS_LessonUpdate'),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/delete', CMS_LessonDelete.as_view(), name='CMS_LessonDelete'),
    path('sorting/topics/<str:topic_slug>/', lessons_sort, name='lessons_sort'),
    path('move/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/up/', lesson_up, name='CMS_LessonUp'),
    path('move/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/down/', lesson_down, name='CMS_LessonDown'),
    path('lessons/<str:lesson_slug>/check_publish/', lesson_check_publish, name='lesson_check_publish'),
]