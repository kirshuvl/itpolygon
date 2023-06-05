from django.urls import path
from cms.constructor.video_step.views import *

urlpatterns = [
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/video/create', CMS_VideoStepCreate.as_view(), name='CMS_VideoStepCreate'),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/video/detail', CMS_VideoStepDetail.as_view(), name='CMS_VideoStepDetail'),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/video/update/', CMS_VideoStepUpdate.as_view(), name='CMS_VideoStepUpdate'),
]
