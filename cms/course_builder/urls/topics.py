from django.urls import path
from cms.course_builder.views.topics import *
urlpatterns = [
    path('courses/<str:course_slug>/create', CMS_TopicCreate.as_view(), name='CMS_TopicCreate'),
    path('courses/<str:course_slug>/<str:topic_slug>/detail', CMS_TopicDetail.as_view(), name='CMS_TopicDetail'),
    path('courses/<str:course_slug>/<str:topic_slug>/update', CMS_TopicUpdate.as_view(), name='CMS_TopicUpdate'),
    path('courses/<str:course_slug>/<str:topic_slug>/delete', CMS_TopicDelete.as_view(), name='CMS_TopicDelete'),
    path('sorting/courses/<str:course_slug>/', topics_sort, name='topics_sort'),
    path('move/<str:course_slug>/<str:topic_slug>/up/', topic_up, name='CMS_TopicUp'),
    path('move/<str:course_slug>/<str:topic_slug>/down/', topic_down, name='CMS_TopicDown'),
    path('topics/<str:topic_slug>/check_publish/', topic_check_publish, name='CMS_TopicPublish'),
]