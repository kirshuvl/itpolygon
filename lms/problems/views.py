
from lms.problems.models import ProblemStep, TestForProblemStep, UserAnswerForProblemStep
from django.views.generic import DetailView, CreateView
from lms.steps.mixins import BaseStepMixin
from lms.problems.forms import ProblemUpload
from django.shortcuts import get_object_or_404


class ProblemStepDetail(BaseStepMixin, CreateView):
    model = ProblemStep
    template_name = 'lms/problems/problem_step_detail.html'
    form_class = ProblemUpload

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['attempts'] = UserAnswerForProblemStep.objects.filter(
            problem=self.object, user=self.request.user)
        context['tests'] = TestForProblemStep.objects.filter(number__lte=self.object.last_sample,
                                                      number__gte=self.object.first_sample,
                                                      problem=self.object).order_by('number')
        return context

    def get_object(self):
        return get_object_or_404(ProblemStep.objects.select_related('lesson__topic__course'),
                                 slug=self.kwargs['step_slug'])

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.problem = ProblemStep.objects.get(
            slug=self.kwargs['step_slug'])

        return super(ProblemStepDetail, self).form_valid(form)


class UserCodeDetail(DetailView):
    model = UserAnswerForProblemStep
    template_name = 'lms/problems/user_answer_detail.html'
    pk_url_kwarg = 'user_answer_pk'
    context_object_name = 'user_answer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Посылка № ' + str(self.object.pk)
        return context
