from django.urls import path
from cms.constructor.text_step.views import *

urlpatterns = [
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/text/create', CMS_TextStepCreate.as_view(), name='CMS_TextStepCreate'),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/text/detail', CMS_TextStepDetail.as_view(), name='CMS_TextStepDetail'),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/text/update/', CMS_TextStepUpdate.as_view(), name='CMS_TextStepUpdate'),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/text/delete/', CMS_TextStepDelete.as_view(), name='CMS_TextStepDelete'),
    
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/text/library', CMS_TextStepFromLibrary.as_view(), name='CMS_TextStepFromLibrary'),
]
