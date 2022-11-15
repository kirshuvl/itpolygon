from django.urls import path
from cms.other.views import *
urlpatterns = [
    path('', CMS_Dashboard.as_view(), name='CMS_Dashboard'),
    path('courses/all', CMS_CoursesList.as_view(), name='CMS_CoursesList'),
    path('courses/my', CMS_UserCoursesList.as_view(), name='CMS_UserCoursesList'),

    # Course

    path('courses/create/', CMS_CourseCreate.as_view(), name='CMS_CourseCreate'),
    path('courses/<str:course_slug>/', CMS_CourseDetail.as_view(), name='CMS_CourseDetail'),
    path('courses/<str:course_slug>/update', CMS_CourseUpdate.as_view(), name='CMS_CourseUpdate'),
    path('courses/<str:course_slug>/delete', CMS_CourseDelete.as_view(), name='CMS_CourseDelete'),
    path('courses/<str:course_slug>/statistics', CMS_CourseStatistics.as_view(), name='CMS_CourseStatistics'),
    path('courses/<str:course_slug>/submissions', CMS_CourseSubmissions.as_view(), name='CMS_CourseSubmissions'),

    # Topic

    path('courses/<str:course_slug>/create', CMS_TopicCreate.as_view(), name='CMS_TopicCreate'),
    path('courses/<str:course_slug>/<str:topic_slug>/', CMS_TopicDetail.as_view(), name='CMS_TopicDetail'),
    path('courses/<str:course_slug>/<str:topic_slug>/update', CMS_TopicUpdate.as_view(), name='CMS_TopicUpdate'),
    path('courses/<str:course_slug>/<str:topic_slug>/delete', CMS_TopicDelete.as_view(), name='CMS_TopicDelete'),

    # Lesson

    path('courses/<str:course_slug>/<str:topic_slug>/create/standart', CMS_LessonCreate.as_view(), name='CMS_LessonCreate'),
    path('courses/<str:course_slug>/<str:topic_slug>/create/quiz', CMS_LessonQuizCreate.as_view(), name='CMS_LessonQuizCreate'),
    path('courses/<str:course_slug>/<str:topic_slug>/create/contest', CMS_LessonContestCreate.as_view(), name='CMS_LessonContestCreate'),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/', CMS_LessonDetail.as_view(), name='CMS_LessonDetail'), 
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/update', CMS_LessonUpdate.as_view(), name='CMS_LessonUpdate'),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/delete', CMS_LessonDelete.as_view(), name='CMS_LessonDelete'),

    # Step

    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/create_text/', CMS_TextStepCreate.as_view(), name='CMS_TextStepCreate'),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/text/', CMS_TextStepDetail.as_view(), name='CMS_TextStepDetail'),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/update_text/', CMS_TextStepUpdate.as_view(), name='CMS_TextStepUpdate'),

    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/create_video/', CMS_VideoStepCreate.as_view(), name='CMS_VideoStepCreate'),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/video/', CMS_VideoStepDetail.as_view(), name='CMS_VideoStepDetail'),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/update_video/', CMS_VideoStepUpdate.as_view(), name='CMS_VideoStepUpdate'),

    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/create_question/', CMS_QuestionStepCreate.as_view(), name='CMS_QuestionStepCreate'),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/question/', CMS_QuestionStepDetail.as_view(), name='CMS_QuestionStepDetail'),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/update_question/', CMS_QuestionStepUpdate.as_view(), name='CMS_QuestionStepUpdate'),

    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/create_problem/', CMS_ProblemStepCreate.as_view(), name='CMS_ProblemStepCreate'),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/problem/', CMS_ProblemStepDetail.as_view(), name='CMS_ProblemStepDetail'),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/update_problem/', CMS_ProblemStepUpdate.as_view(), name='CMS_ProblemStepUpdate'),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/problem/create_tests', CMS_ProblemStepCreateTests.as_view(), name='CMS_ProblemStepCreateTests'),

    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/create_assignment/', CMS_AssignmentStepCreate.as_view(), name='CMS_AssignmentStepCreate'),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/assignment/', CMS_AssignmentSteppDetail.as_view(), name='CMS_AssignmentStepDetail'),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/update_assignment/', CMS_AssignmentStepUpdate.as_view(), name='CMS_AssignmentStepUpdate'),

    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/delete/', CMS_StepDelete.as_view(), name='CMS_StepDelete'),

    path('course/<str:course_slug>/check_publish/', course_check_publish, name='course_check_publish'),
    path('topics/<str:topic_slug>/check_publish/', topic_check_publish, name='topic_check_publish'),
    path('lessons/<str:lesson_slug>/check_publish/', lesson_check_publish, name='lesson_check_publish'),
    path('steps/<str:step_slug>/check_publish/', step_check_publish, name='step_check_publish'),

    path('sorting/courses/<str:course_slug>/', topics_sort, name='topics_sort'),
    path('sorting/topics/<str:topic_slug>/', lessons_sort, name='lessons_sort'),
    path('sorting/steps/<str:lesson_slug>/', steps_sort, name='steps_sort'),

    path('move/<str:course_slug>/<str:topic_slug>/up/', topic_up, name='topic_up'),
    path('move/<str:course_slug>/<str:topic_slug>/down/', topic_down, name='topic_down'),

    path('move/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/up/', lesson_up, name='lesson_up'),
    path('move/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/down/', lesson_down, name='lesson_down'),

    path('move/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/up/', step_up, name='step_up'),
    path('move/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/down/', step_down, name='step_down'),
]
