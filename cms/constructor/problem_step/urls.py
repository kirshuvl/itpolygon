from django.urls import path, include
from cms.constructor.problem_step.views import *

urlpatterns = [
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/problem/create/', CMS_ProblemStepCreate.as_view(), name='CMS_ProblemStepCreate'),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/problem/detail/', CMS_ProblemStepDetail.as_view(), name='CMS_ProblemStepDetail'),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/problem/update/', CMS_ProblemStepUpdate.as_view(), name='CMS_ProblemStepUpdate'),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/problem/tests/', CMS_ProblemStepCreateTests.as_view(), name='CMS_ProblemStepCreateTests'),
]
