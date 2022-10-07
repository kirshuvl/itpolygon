from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, DetailView, DeleteView, UpdateView
from crm.lead.forms import UserLeadForm, LeadCommentForm, UserLeadFormUpdate
from crm.lead.models import UserLead, LeadComment, Status, UserFeedBack
from lms.courses.models import Course
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class CRMDashboard(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'crm/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(CRMDashboard, self).get_context_data(**kwargs)
        context['page_title'] = 'CRM Dashboard'

        return context

    def get_permission_required(self):
        return 'lead.view_userfeedback', 'lead.view_userlead'


class FeedBackAllList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = UserFeedBack
    template_name = 'crm/lead/feedback_list.html'
    context_object_name = 'feedbacks'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(FeedBackAllList, self).get_context_data(**kwargs)
        context['page_title'] = 'Все заявки пользователей'
        return context

    def get_queryset(self):
        return UserFeedBack.objects.prefetch_related('status').order_by('-date_create')

    def get_permission_required(self):
        return 'lead.view_userfeedback',


class FeedBackNewList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = UserFeedBack
    template_name = 'crm/lead/feedback_list.html'
    context_object_name = 'feedbacks'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(FeedBackNewList, self).get_context_data(**kwargs)
        context['page_title'] = 'Новые заявки пользователей'
        return context

    def get_queryset(self):
        return UserFeedBack.objects.prefetch_related('status').filter(status__title='Новая заявка').\
            order_by('-date_create')

    def get_permission_required(self):
        return 'lead.view_userfeedback',


class LeadAllList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = UserLead
    template_name = 'crm/lead/lead_list.html'
    context_object_name = 'leads'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(LeadAllList, self).get_context_data(**kwargs)
        context['page_title'] = 'Все записи на курсы'
        return context

    def get_queryset(self):
        return UserLead.objects.prefetch_related('status').order_by('-date_create')

    def get_permission_required(self):
        return 'lead.view_userlead',


class LeadNewList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = UserLead
    template_name = 'crm/lead/lead_list.html'
    context_object_name = 'leads'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(LeadNewList, self).get_context_data(**kwargs)
        context['page_title'] = 'Новые записи на курсы'
        return context

    def get_queryset(self):
        return UserLead.objects.prefetch_related('status').filter(status__title='Новая заявка').order_by('-date_create')

    def get_permission_required(self):
        return 'lead.view_userlead',


class LeadDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = UserLead
    template_name = 'crm/lead/lead_detail.html'
    context_object_name = 'lead'

    def get_context_data(self, **kwargs):
        context = super(LeadDetail, self).get_context_data(**kwargs)
        context['page_title'] = 'Просмотр заявки'

        return context

    def get_object(self, queryset=None):
        return get_object_or_404(UserLead.objects.prefetch_related('leadcomments__status',
                                                                   'leadcomments__author'), pk=self.kwargs['lead_pk'])

    def get_permission_required(self):
        return 'lead.view_userlead', 'lead.view_leadcomment',


class LeadUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = UserLead
    form_class = UserLeadFormUpdate
    template_name = 'crm/lead/lead_update.html'
    context_object_name = 'lead'
    pk_url_kwarg = 'lead_pk'

    def get_object(self, queryset=None):
        return get_object_or_404(UserLead.objects.prefetch_related('leadcomments__status',
                                                                   'leadcomments__author'), pk=self.kwargs['lead_pk'])

    def get_permission_required(self):
        return 'lead.view_userlead', 'lead.change_userlead', 'lead.view_leadcomment',


class LeadCommentCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = LeadComment
    form_class = LeadCommentForm
    template_name = 'crm/lead/leadcomment_create.html'

    def get_context_data(self, **kwargs):
        context = super(LeadCommentCreate, self).get_context_data(**kwargs)
        context['page_title'] = 'Добавить комментарий к заявке'
        context['lead'] = get_object_or_404(UserLead.objects.prefetch_related('leadcomments__status',
                                                                              'leadcomments__author'),
                                            pk=self.kwargs['lead_pk'])

        return context

    def form_valid(self, form):
        form.instance.lead = UserLead.objects.get(pk=self.kwargs['lead_pk'])
        form.instance.author = self.request.user
        lead = get_object_or_404(
            UserLead.objects.all(), pk=self.kwargs['lead_pk'])
        lead.status = form.cleaned_data.get('status')
        lead.save()
        return super(LeadCommentCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('LeadDetail', kwargs={'lead_pk': self.kwargs['lead_pk']})

    def get_permission_required(self):
        return 'lead.view_leadcomment', 'lead.add_leadcomment',


class LeadCommentDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = LeadComment
    template_name = 'crm/lead/leadcomment_delete.html'
    context_object_name = 'comment'

    def get_context_data(self, **kwargs):
        context = super(LeadCommentDelete, self).get_context_data(**kwargs)
        context['page_title'] = 'Удалить комментарий к заявке'
        context['lead'] = get_object_or_404(UserLead.objects.prefetch_related('leadcomments__status',
                                                                              'leadcomments__author'),
                                            pk=self.kwargs['lead_pk'])

        return context

    def get_object(self, queryset=None):
        return get_object_or_404(LeadComment.objects.all(), pk=self.kwargs['ticket_pk'])

    def get_success_url(self):
        return reverse_lazy('LeadDetail', kwargs={'lead_pk': self.kwargs['lead_pk']})

    def get_permission_required(self):
        return 'lead.view_leadcomment', 'lead.delete_leadcomment',


class LeadCommentUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = LeadComment
    form_class = LeadCommentForm
    template_name = 'crm/lead/leadcomment_update.html'
    pk_url_kwarg = 'ticket_pk'

    def get_context_data(self, **kwargs):
        context = super(LeadCommentUpdate, self).get_context_data(**kwargs)
        context['page_title'] = 'Редактировать комментарий к заявке'
        context['lead'] = get_object_or_404(UserLead.objects.prefetch_related('leadcomments__status',
                                                                              'leadcomments__author'),
                                            pk=self.kwargs['lead_pk'])

        return context

    def form_valid(self, form):
        all_comments = LeadComment.objects.filter(
            lead=self.object.lead).order_by('-date_create')
        if self.object == all_comments.first():
            lead = get_object_or_404(
                UserLead.objects.all(), pk=self.kwargs['lead_pk'])
            lead.status = self.object.status
            lead.save()

        return super(LeadCommentUpdate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('LeadDetail', kwargs={'lead_pk': self.kwargs['lead_pk']})

    def get_permission_required(self):
        return 'lead.view_leadcomment', 'lead.change_leadcomment',


class LandingPage(CreateView):
    model = UserLead
    form_class = UserLeadForm
    template_name = 'crm/lead/landing.html'

    def get_context_data(self, **kwargs):
        context = super(LandingPage, self).get_context_data(**kwargs)
        context['course'] = get_object_or_404(Course.objects.prefetch_related('skills'),
                                              slug=self.kwargs['course_slug'])

        return context

    def form_valid(self, form):
        form.instance.course = Course.objects.get(
            slug=self.kwargs['course_slug'])
        try:
            form.instance.status = Status.objects.get(title='Новая заявка')
        except Status.DoesNotExist:
            form.instance.status = None
        messages.add_message(self.request, messages.SUCCESS,
                             'Отлично! Ваша заявка принята. Мы свяжемся с Вами в ближайшее время. Но если произойдет '
                             'сбой и мы не напишем - смело пишите нам')

        if form.instance.promocode is not None:
            messages.add_message(self.request, messages.SUCCESS,
                                 'Вы успешно применили промокод. Итоговую цену Вам сообщит менеджер')

        return super(LandingPage, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('LandingPage', kwargs={'course_slug': self.kwargs['course_slug']})
