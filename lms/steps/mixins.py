from django.views.generic import DetailView
from lms.achievements.models import StepAchievement
from lms.steps.models import Step, StepEnroll
from django.db.models import Q
from django.http import HttpResponseRedirect


class BaseStepMixin(DetailView):
    context_object_name = 'step'
    slug_url_kwarg = 'step_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['steps'] = Step.objects.prefetch_related('lesson__topic__course', 'steps_enrolls__user',).\
            filter(is_published=True).\
            filter(Q(TextStep___lesson=self.object.lesson) |
                   Q(VideoStep___lesson=self.object.lesson) |
                   Q(QuestionStep___lesson=self.object.lesson)).\
            order_by('number')
        context['page_title'] = self.object.title
        context['attempts'] = None
        self.user_start_step()

        return context

    def user_start_step(self):
        StepEnroll.objects.get_or_create(
            step=self.object,
            user=self.request.user
        )

    def user_end_step(request, course_slug, topic_slug, lesson_slug, step_slug):
        step_enroll = StepEnroll.objects.get(
            step=Step.objects.get(slug=step_slug), user=request.user)
        if step_enroll.status == 'PR' or step_enroll.status == 'RP':
            step_enroll.status = 'OK'
            StepAchievement.objects.get_or_create(user=request.user,
                                                  points=step_enroll.step.points,
                                                  for_what=step_enroll.step,
                                                  )
            request.user.coin += step_enroll.step.points
            request.user.save()
            step_enroll.save()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
