from typing import Any, Optional
from django.db import models
from django.views.generic import DetailView, ListView, TemplateView
from lms.achievements.models import StepAchievement
from lms.steps.models import Step, StepEnroll, LessonStepConnection
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch


class BaseStepMixin(ListView):
    model = Step
    context_object_name = 'steps'
    slug_url_kwarg = 'step_slug'

    def get(self, request, *args, **kwargs):
        self.object_list = list(self.get_queryset())
        self.object = self.get_object()
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.user_start_step()
        context['step'] = self.object
        context['attempts'] = None
        return context

    def get_queryset(self):
        queryset = Step.objects.\
            filter(connections__lesson__slug=self.kwargs['lesson_slug'], connections__is_published=True).\
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
        StepEnroll.objects.get_or_create(
            step__slug=self.kwargs['step_slug'],
            user=self.request.user
        )

    def user_end_step(request, course_slug, topic_slug, lesson_slug, step_slug):
        step_enroll = StepEnroll.objects.get(
            step__slug=step_slug, user=request.user)
        if step_enroll.status == 'PR' or step_enroll.status == 'RP':
            step_enroll.status = 'OK'
            step_enroll.save()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


'''
class BaseStepMixin(TemplateView):
    model = Step
    context_object_name = 'steps'
    slug_url_kwarg = 'step_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['attempts'] = None
        context['steps'], context['step'] = self.get_data()
        return context

    def get_steps(self):
        queryset = Step.objects.\
            filter(connections__lesson__slug=self.kwargs['lesson_slug'], connections__is_published=True).\
            prefetch_related(
                Prefetch('connections', queryset=LessonStepConnection.objects.filter(
                    lesson__slug=self.kwargs['lesson_slug'])),
                Prefetch('steps_enrolls',
                         queryset=StepEnroll.objects.select_related('user').filter(user=self.request.user))).order_by('connections__number')
        return queryset
    
    def get_data(self):
        data = self.get_steps()

        steps = []
        step = None

        for el in data:
            steps.append(el)
            if el.slug == self.kwargs['step_slug']:
                step = el

        return steps, step

    # def get_queryset(self):
    #    if not hasattr(self, '_cached_queryset'):
    #        self._cached_queryset = self.get_steps()
    #    return self._cached_queryset

    def get_object(self, queryset=None):
        print('get_object_start')
        #Step.objects.prefetch_related(Prefetch('steps_enrolls',
        #                 queryset=StepEnroll.objects.select_related('user').filter(user=self.request.user)))
        print('get_object_start')
        return get_object_or_404(queryset, slug=self.kwargs['step_slug'])

    def user_start_step(self):
        StepEnroll.objects.get_or_create(
            step__slug=self.kwargs['step_slug'],
            user=self.request.user
        )

    def user_end_step(request, course_slug, topic_slug, lesson_slug, step_slug):
        step_enroll = StepEnroll.objects.get(
            step__slug=step_slug, user=request.user)
        if step_enroll.status == 'PR' or step_enroll.status == 'RP':
            step_enroll.status = 'OK'
            step_enroll.save()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
'''
