from django.urls import path
from crm.lead.views import CRMDashboard, FeedBackAllList, FeedBackNewList, LeadAllList, LeadNewList, LeadDetail, LeadUpdate, LeadCommentCreate, LeadCommentDelete, LeadCommentUpdate

urlpatterns = [
    path('', CRMDashboard.as_view(), name='CRMDashboard'),
    path('feedback/all', FeedBackAllList.as_view(), name='FeedBackAllList'),
    path('feedback/new', FeedBackNewList.as_view(), name='FeedBackNewList'),
    path('lead/all/', LeadAllList.as_view(), name='LeadAllList'),
    path('lead/new/', LeadNewList.as_view(), name='LeadNewList'),
    path('lead/all/<lead_pk>/', LeadDetail.as_view(), name='LeadDetail'),
    path('lead/all/<lead_pk>/update_lead',
         LeadUpdate.as_view(), name='LeadUpdate'),
    path('lead/all/<lead_pk>/new_ticket',
         LeadCommentCreate.as_view(), name='LeadCommentCreate'),
    path('lead/all/<lead_pk>/<ticket_pk>/delete_ticket',
         LeadCommentDelete.as_view(), name='LeadCommentDelete'),
    path('lead/all/<lead_pk>/<ticket_pk>/update_ticket',
         LeadCommentUpdate.as_view(), name='LeadCommentUpdate'),
]
