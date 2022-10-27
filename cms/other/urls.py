from django.urls import path
from cms.other.views import CMS_Dashboard, CMS_CoursesList, CMS_CourseCreate, CMS_ProblemStepCreate, CMS_ProblemStepDetail, CMS_QuestionStepCreate, CMS_QuestionStepDetail, CMS_TextStepCreate, CMS_TextStepDetail, CMS_TopicCreate,\
    CMS_UserCoursesList, CMS_CourseUpdate, CMS_CourseDelete, CMS_CourseDetail, CMS_LessonCreate, \
        CMS_LessonQuizCreate, CMS_LessonContestCreate, CMS_LessonDetail, CMS_VideoStepCreate, CMS_VideoStepDetail

urlpatterns = [
    path('', CMS_Dashboard.as_view(), name='CMS_Dashboard'),
    path('courses/all', CMS_CoursesList.as_view(), name='CMS_CoursesList'),
    path('courses/my', CMS_UserCoursesList.as_view(), name='CMS_UserCoursesList'),
    path('courses/create/', CMS_CourseCreate.as_view(), name='CMS_CourseCreate'),
    
    path('courses/<str:course_slug>/update', CMS_CourseUpdate.as_view(), name='CMS_CourseUpdate'),
    path('courses/<str:course_slug>/delete', CMS_CourseDelete.as_view(), name='CMS_CourseDelete'),

    path('courses/<str:course_slug>/create', CMS_TopicCreate.as_view(), name='CMS_TopicCreate'),

    path('courses/<str:course_slug>/<str:topic_slug>/create_lesson', CMS_LessonCreate.as_view(), name='CMS_LessonCreate'),
    path('courses/<str:course_slug>/<str:topic_slug>/create_quiz', CMS_LessonQuizCreate.as_view(), name='CMS_LessonQuizCreate'),
    path('courses/<str:course_slug>/<str:topic_slug>/create_contest', CMS_LessonContestCreate.as_view(), name='CMS_LessonContestCreate'),

    path('courses/<str:course_slug>/', CMS_CourseDetail.as_view(), name='CMS_CourseDetail'),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/', CMS_LessonDetail.as_view(), name='CMS_LessonDetail'),


    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/create_text', CMS_TextStepCreate.as_view(), name='CMS_TextStepCreate'),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/create_video', CMS_VideoStepCreate.as_view(), name='CMS_VideoStepCreate'),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/create_question', CMS_QuestionStepCreate.as_view(), name='CMS_QuestionStepCreate'),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/create_problem', CMS_ProblemStepCreate.as_view(), name='CMS_ProblemStepCreate'),

    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/text', CMS_TextStepDetail.as_view(), name='CMS_TextStepDetail'),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/video', CMS_VideoStepDetail.as_view(), name='CMS_VideoStepDetail'),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/question', CMS_QuestionStepDetail.as_view(), name='CMS_QuestionStepDetail'),
    path('courses/<str:course_slug>/<str:topic_slug>/<str:lesson_slug>/<str:step_slug>/problem', CMS_ProblemStepDetail.as_view(), name='CMS_ProblemStepDetail'),
]
