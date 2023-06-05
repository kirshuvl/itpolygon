from django.urls import path, include
from cms.constructor.question_choice_step.views import *
urlpatterns = [
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/question_choice/create', CMS_QuestionChoiceStepCreate.as_view(), name='CMS_QuestionChoiceStepCreate'),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/question_choice/detail', CMS_QuestionChoiceStepDetail.as_view(), name='CMS_QuestionChoiceStepDetail'),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/question_choice/update', CMS_QuestionChoiceStepUpdate.as_view(), name='CMS_QuestionChoiceStepUpdate'),
]
