from django.urls import path
from cms.constructor.question_step.views import *

urlpatterns = [
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/question/create/', CMS_QuestionStepCreate.as_view(), name='CMS_QuestionStepCreate'),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/question/detail/', CMS_QuestionStepDetail.as_view(), name='CMS_QuestionStepDetail'),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/question/update/', CMS_QuestionStepUpdate.as_view(), name='CMS_QuestionStepUpdate'),
]
