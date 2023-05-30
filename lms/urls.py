from django.urls import path, include
from lms.achievements.views import UserAchievements
from lms.assignment.views import AssignmentStepDetail

from lms.homeworks.views import UserHomeworkList, UserHomeworkDetail
from lms.lessons.views import LessonStatistics
from lms.steps.mixins import BaseStepMixin
from lms.problems.views import ProblemStepDetail, UserCodeDetail


urlpatterns = [
    path('', include('lms.courses.urls')),
    path('', include('lms.lessons.urls')),
    path('', include('lms.steps.urls')),





    path('achievements/my', UserAchievements.as_view(), name='UserAchievementsList'),

    path('submissions/<int:user_answer_pk>/', UserCodeDetail.as_view(), name='UserCodeDetail'),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/pass',
         BaseStepMixin.user_end_step, name='UserEndStep'),
    path('homeworks/my', UserHomeworkList.as_view(), name='UserHomeworkList'),
    path('homeworks/my/<int:homework_pk>/',
         UserHomeworkDetail.as_view(), name='UserHomeworkDetail')
]
