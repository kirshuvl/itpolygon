from django.shortcuts import render
from django.views.generic import DetailView, ListView
from lms.homeworks.models import Homework, HomeworkStepConnection
from django.db.models import Prefetch
from lms.lessons.models import Lesson
from lms.steps.models import Step, StepEnroll, LessonStepConnection
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404


class LMS_UserHomeworkList(LoginRequiredMixin, ListView):
    model = Homework
    template_name = 'lms/homeworks/list.html'
    context_object_name = 'homeworks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Домашние задания'

        return context

    def get_queryset(self):
        return Homework.objects.filter(user=self.request.user).select_related('course').prefetch_related(
            Prefetch('h_connections', queryset=HomeworkStepConnection.objects.select_related('step').prefetch_related(
                Prefetch('step__steps_enrolls', queryset=StepEnroll.objects.select_related(
                    'user').filter(user=self.request.user))
            )),
        ).order_by('date_to')


class LMS_UserHomeworkDetail(LoginRequiredMixin, DetailView):
    model = Homework
    template_name = 'lms/homeworks/detail.html'
    context_object_name = 'homework'
    pk_url_kwarg = 'pk'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Домашнее задание'
        context['steps'] = self.get_steps()

        return context

    def get_steps(self):
        homework: Homework = self.object
        queryset = Step.objects.filter(h_connections__homework__pk=self.kwargs['pk']).prefetch_related(
            Prefetch('connections', queryset=LessonStepConnection.objects.filter(
                lesson__topic__course=homework.course)),
            Prefetch('steps_enrolls',
                     queryset=StepEnroll.objects.select_related('user').filter(user=self.request.user))
        ).order_by('h_connections__number')

        return queryset
