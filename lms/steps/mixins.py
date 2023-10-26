from django.db import models
from django.views.generic import DetailView, ListView, TemplateView
from lms.achievements.models import StepAchievement
from lms.steps.models import Step, StepEnroll, LessonStepConnection
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from django.contrib.auth.mixins import LoginRequiredMixin

class BaseStepMixin(LoginRequiredMixin, ListView):
    model = Step
    context_object_name = 'steps'
    slug_url_kwarg = 'step_slug'

    def get(self, request, *args, **kwargs):
        self.user_start_step()
        self.object_list = list(self.get_queryset())
        self.object = self.get_object()
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['step'] = self.object
        context['page_title'] = self.object.title
        return context

    def get_queryset(self):
        queryset = Step.objects.\
            filter(connections__lesson__slug=self.kwargs['lesson_slug'], connections__is_published=True).select_related('author').\
            prefetch_related(
                Prefetch('connections', queryset=LessonStepConnection.objects.filter(
                    lesson__slug=self.kwargs['lesson_slug'])),
                Prefetch('steps_enrolls',
                         queryset=StepEnroll.objects.select_related('user').filter(user=self.request.user))).order_by('connections__number')
        
        return queryset

    def get_object(self):
        for step in self.object_list:
            if step.slug == self.kwargs['step_slug']:
                return step
        return

    def user_start_step(self):
        StepEnroll.objects.get_or_create(step=Step.objects.get(
            slug=self.kwargs['step_slug']), user=self.request.user)

    def user_end_step(request, course_slug, topic_slug, lesson_slug, step_slug):
        step_enroll = StepEnroll.objects.get(
            step__slug=step_slug, user=request.user)
        if step_enroll.status == 'PR' or step_enroll.status == 'RP':
            step_enroll.status = 'OK'
            step_enroll.save()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

    def form_invalid(self, form):
        self.object_list = list(self.get_queryset())
        self.object = self.get_object()
        context = self.get_context_data()
        return self.render_to_response(self.get_context_data())
