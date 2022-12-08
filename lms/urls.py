from django.urls import path, include
from lms.achievements.views import UserAchievements
from lms.assignment.views import AssignmentStepDetail
from lms.courses.views import CoursesList, UserCoursesList, CourseDetail
from lms.homeworks.views import UserHomeworkList, UserHomeworkDetail
from lms.lessons.views import LessonDetail, LessonStatistics
from lms.steps.mixins import BaseStepMixin
from lms.steps.views import QuestionChoiceStepDetail, TextStepDetail, VideoStepDetail, QuestionStepDetail
from lms.problems.views import ProblemStepDetail, UserCodeDetail


urlpatterns = [
    path('courses/all', CoursesList.as_view(), name='CoursesList'),
    path('courses/my', UserCoursesList.as_view(), name='UserCoursesList'),
    path('achievements/my', UserAchievements.as_view(),
         name='UserAchievementsList'),
    path('courses/<str:course_slug>/',
         CourseDetail.as_view(),
         name='CourseDetail'
         ),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/',
         LessonDetail.as_view(),
         name='LessonDetail'
         ),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/text/',
         TextStepDetail.as_view(),
         name='TextStepDetail'
         ),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/video/',
         VideoStepDetail.as_view(),
         name='VideoStepDetail'
         ),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/question/',
         QuestionStepDetail.as_view(),
         name='QuestionStepDetail'
         ),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/question/choice/',
         QuestionChoiceStepDetail.as_view(),
         name='QuestionChoiceStepDetail'
         ),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/problem/',
         ProblemStepDetail.as_view(),
         name='ProblemStepDetail'
         ),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/assignment/',
         AssignmentStepDetail.as_view(),
         name='AssignmentStepDetail'
         ),
    path('submissions/<int:user_answer_pk>/',
         UserCodeDetail.as_view(),
         name='UserCodeDetail'
         ),
    path('lessons/statistics/<str:lesson_slug>/',
         LessonStatistics.as_view(),
         name='LessonStatistics'),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/pass',
         BaseStepMixin.user_end_step,
         name='UserEndStep'
         ),
    path('homeworks/my', UserHomeworkList.as_view(), name='UserHomeworkList'),
    path('homeworks/my/<int:homework_pk>/',
         UserHomeworkDetail.as_view(), name='UserHomeworkDetail')
]
