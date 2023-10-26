from django.views.generic import DetailView
from lms.lessons.models import Lesson
from lms.steps.models import Step, StepEnroll, LessonStepConnection
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from django.contrib.auth.mixins import LoginRequiredMixin

class LMS_LessonDetail(LoginRequiredMixin, DetailView):
    model = Lesson
    template_name = 'lms/lessons/detail.html'
    slug_url_kwarg = 'lesson_slug'
    context_object_name = 'lesson'

    def get_context_data(self, **kwargs):
        context = super(LMS_LessonDetail, self).get_context_data()
        context['page_title'] = f'{self.object.title} - ИТ Полигон'
        context['steps'] = self.get_steps()

        return context

    def get_steps(self):
        queryset = Step.objects.\
            filter(connections__lesson__slug=self.kwargs['lesson_slug'], connections__is_published=True).\
            prefetch_related(
                Prefetch('connections',
                         queryset=LessonStepConnection.objects.filter(lesson__slug=self.kwargs['lesson_slug'])),
                Prefetch('steps_enrolls',
                         queryset=StepEnroll.objects.select_related('user').filter(user=self.request.user))).order_by('connections__number')

        return queryset

    def get_object(self):

        return get_object_or_404(Lesson.objects.all(), slug=self.kwargs['lesson_slug'])
