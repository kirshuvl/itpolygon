from django.urls import path, include
from cms.constructor.assignment_step.views import *

urlpatterns = [
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/create_assignment/', CMS_AssignmentStepCreate.as_view(), name='CMS_AssignmentStepCreate'),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/assignment/', CMS_AssignmentSteppDetail.as_view(), name='CMS_AssignmentStepDetail'),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/update_assignment/', CMS_AssignmentStepUpdate.as_view(), name='CMS_AssignmentStepUpdate'),
]
