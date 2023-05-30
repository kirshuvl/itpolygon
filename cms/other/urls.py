from django.urls import path, include
from cms.other.views import *
urlpatterns = [
    path('', CMS_Dashboard.as_view(), name='CMS_Dashboard'), # + 
    path('courses/assignments/my', CMS_UserAssignmentsList.as_view(), name='CMS_UserAssignmentsList'),
    # Course
    path('courses/<str:course_slug>/statistics', CMS_CourseStatistics.as_view(), name='CMS_CourseStatistics'),
    path('courses/<str:course_slug>/submissions', CMS_CourseSubmissions.as_view(), name='CMS_CourseSubmissions'),
    # Step
    path('steps/<str:step_slug>/check_publish/', step_check_publish, name='step_check_publish'),
    path('submissions/<int:user_answer_pk>/rerun', rerun_submission, name='rerun_submissions'),
]
