from django.shortcuts import render
from django.views.generic import DetailView, ListView
from lms.homeworks.models import Homework
from django.db.models import Prefetch
from lms.lessons.models import Lesson
from lms.steps.models import Step, StepEnroll




class UserHomeworkList(ListView):
    model = Homework
    template_name = 'lms/homeworks/user_homework_list.html'
    context_object_name = 'homeworks'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserHomeworkList, self).get_context_data(**kwargs)
        context['page_title'] = 'Домашние задания'
        
        return context

    def get_queryset(self):
        return Homework.objects.prefetch_related(Prefetch('steps__steps_enrolls', queryset=StepEnroll.objects.filter(user=self.request.user))).select_related('course').filter(user=self.request.user, is_done=False)


class UserHomeworkDetail(DetailView):
    model = Homework
    template_name = 'lms/homeworks/homework_detail.html'
    context_object_name = 'homework'
    pk_url_kwarg = 'homework_pk'

