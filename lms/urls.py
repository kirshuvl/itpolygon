from django.urls import path, include
from lms.achievements.views import UserAchievements
from lms.courses.views import CoursesList, UserCoursesList, CourseDetail
from lms.lessons.views import LessonDetail, LessonStatistics
from lms.steps.mixins import BaseStepMixin
from lms.steps.views import TextStepDetail, VideoStepDetail, QuestionStepDetail

urlpatterns = [
    path('courses/all',
         CoursesList.as_view(),
         name='CoursesList'
         ),
    path('courses/my',
         UserCoursesList.as_view(),
         name='UserCoursesList'
         ),
    path('achievements/my',
         UserAchievements.as_view(),
         name='UserAchievementsList'
         ),
    path('courses/<str:course_slug>/',
         CourseDetail.as_view(),
         name='CourseDetail'
         ),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/',
         LessonDetail.as_view(),
         name='LessonDetail'
         ),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/text',
         TextStepDetail.as_view(),
         name='TextStepDetail'
         ),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/video',
         VideoStepDetail.as_view(),
         name='VideoStepDetail'
         ),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/question',
         QuestionStepDetail.as_view(),
         name='QuestionStepDetail'
         ),
    path('lessons/statistics/<str:lesson_slug>/',
         LessonStatistics.as_view(),
         name='LessonStatistics'),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/pass',
         BaseStepMixin.user_end_step,
         name='UserEndStep'
         ),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/pass',
         LessonDetail.user_end_lesson,
         name='UserEndLesson'
         ),
]
