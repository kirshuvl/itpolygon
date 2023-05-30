from django.urls import path
from lms.assignment.views import AssignmentStepDetail
from lms.steps.views import LMS_QuestionChoiceStepDetail, LMS_TextStepDetail, LMS_VideoStepDetail, LMS_QuestionStepDetail
from lms.problems.views import ProblemStepDetail, UserCodeDetail


urlpatterns = [
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/text/', LMS_TextStepDetail.as_view(), name='LMS_TextStepDetail'),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/video/',LMS_VideoStepDetail.as_view(),name='LMS_VideoStepDetail'),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/question/',LMS_QuestionStepDetail.as_view(),name='LMS_QuestionStepDetail'),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/question/choice/',LMS_QuestionChoiceStepDetail.as_view(), name='LMS_QuestionChoiceStepDetail'),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/problem/',ProblemStepDetail.as_view(),name='ProblemStepDetail'),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/assignment/',AssignmentStepDetail.as_view(),name='AssignmentStepDetail'),
]
