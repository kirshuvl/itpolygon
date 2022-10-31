from django.views.generic import DetailView
from lms.achievements.models import StepAchievement
from lms.steps.models import Step, StepEnroll
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch


class BaseStepMixin(DetailView):
    context_object_name = 'step'
    slug_url_kwarg = 'step_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.user_start_step()
        context['steps'] = self.queryset
        context['page_title'] = self.object.title
        context['attempts'] = None

        return context

    def get_queryset(self):
        self.queryset = Step.objects.select_related('lesson__topic__course').\
            prefetch_related(
                Prefetch('steps_enrolls', queryset=StepEnroll.objects.filter(
                    user=self.request.user))
        ).filter(lesson__slug=self.kwargs['lesson_slug'], is_published=True).order_by('number')
        return self.queryset

    def get_object(self):
        self.queryset = self.get_queryset()

        return self.queryset.get(slug=self.kwargs['step_slug'])

    def user_start_step(self):
        StepEnroll.objects.get_or_create(
            step=self.object,
            user=self.request.user
        )

    def user_end_step(request, course_slug, topic_slug, lesson_slug, step_slug):
        step_enroll = StepEnroll.objects.get(
            step__slug=step_slug, user=request.user)
        if step_enroll.status == 'PR' or step_enroll.status == 'RP':
            step_enroll.status = 'OK'
            step_enroll.save()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
