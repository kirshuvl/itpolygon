from django.urls import path
from cms.course_builder.views.steps import *


urlpatterns = [
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/create_text/', CMS_TextStepCreate.as_view(), name='CMS_TextStepCreate'),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/create_video/', CMS_VideoStepCreate.as_view(), name='CMS_VideoStepCreate'),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/create_question/', CMS_QuestionStepCreate.as_view(), name='CMS_QuestionStepCreate'),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/create_problem/', CMS_ProblemStepCreate.as_view(), name='CMS_ProblemStepCreate'),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/create_assignment/', CMS_AssignmentStepCreate.as_view(), name='CMS_AssignmentStepCreate'),

    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/text/', CMS_TextStepDetail.as_view(), name='CMS_TextStepDetail'),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/update_text/', CMS_TextStepUpdate.as_view(), name='CMS_TextStepUpdate'),

    
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/video/', CMS_VideoStepDetail.as_view(), name='CMS_VideoStepDetail'),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/update_video/', CMS_VideoStepUpdate.as_view(), name='CMS_VideoStepUpdate'),

    
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/question/', CMS_QuestionStepDetail.as_view(), name='CMS_QuestionStepDetail'),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/update_question/', CMS_QuestionStepUpdate.as_view(), name='CMS_QuestionStepUpdate'),

    
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/problem/', CMS_ProblemStepDetail.as_view(), name='CMS_ProblemStepDetail'),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/update_problem/', CMS_ProblemStepUpdate.as_view(), name='CMS_ProblemStepUpdate'),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/problem/create_tests', CMS_ProblemStepCreateTests.as_view(), name='CMS_ProblemStepCreateTests'),

    
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/assignment/', CMS_AssignmentSteppDetail.as_view(), name='CMS_AssignmentStepDetail'),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/update_assignment/', CMS_AssignmentStepUpdate.as_view(), name='CMS_AssignmentStepUpdate'),

    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/delete/', CMS_StepDelete.as_view(), name='CMS_StepDelete'),
    
    path('sorting/steps/<str:lesson_slug>/', connect_sort, name='steps_sort'),
    path('connections/<str:lesson_slug>/<int:pk>/up', connect_up, name='connect_up'),
    path('connections/<str:lesson_slug>/<int:pk>/down/', connect_down, name='connect_down'),
]

