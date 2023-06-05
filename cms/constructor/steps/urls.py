from django.urls import path, include
from cms.constructor.steps.views import *

urlpatterns = [
    path('', include('cms.constructor.text_step.urls')),
    path('', include('cms.constructor.video_step.urls')),
    path('', include('cms.constructor.question_step.urls')),
    path('', include('cms.constructor.question_choice_step.urls')),
    path('', include('cms.constructor.problem_step.urls')),
    path('', include('cms.constructor.assignment_step.urls')),

    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/delete/', CMS_StepDelete.as_view(), name='CMS_StepDelete'),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/move_up/', connect_up, name='CMS_ConnectUp'),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/move_down/', connect_down, name='CMS_ConnectDown'),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/check_publish/', connect_check_publish, name='CMS_ConnectPublish'),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/connect/create/', connect_create, name='CMS_ConnectCreate'),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/connect/delete/', connect_delete, name='CMS_ConnectDelete'),
]
