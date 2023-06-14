from django.urls import path, include
from lms.achievements.views import UserAchievements

from lms.steps.mixins import BaseStepMixin
from lms.problems.views import LMS_UserCodeDetail


urlpatterns = [
    path('', include('lms.courses.urls')),
    path('', include('lms.lessons.urls')),
    path('', include('lms.steps.urls')),
    path('', include('lms.homeworks.urls')),





    path('achievements/my', UserAchievements.as_view(),
         name='UserAchievementsList'),

    path('submissions/<int:user_answer_pk>/',
         LMS_UserCodeDetail.as_view(), name='LMS_UserCodeDetail'),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/pass',
         BaseStepMixin.user_end_step, name='UserEndStep'),
    
]
