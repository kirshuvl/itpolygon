
from lms.problems.models import ProblemStep, TestForProblemStep, UserAnswerForProblemStep
from django.views.generic import DetailView, CreateView
from lms.steps.mixins import BaseStepMixin
from lms.problems.forms import ProblemUpload
from django.shortcuts import get_object_or_404
from lms.steps.models import Step

class ProblemStepDetail(BaseStepMixin, CreateView):
    template_name = 'lms/problems/problem_step_detail.html'
    form_class = ProblemUpload

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self)
        context['tests'] = TestForProblemStep.objects.filter(number__lte=self.object.last_sample,
                                                             number__gte=self.object.problem.first_sample,
                                                             problem=self.object.problem).order_by('number')
        
        if self.request.user.is_superuser:
            context['users_attempts'] = UserAnswerForProblemStep.objects.select_related('problem__lesson__topic__course', 'user').filter(
                problem=self.object)
            context['attempts'] = context['users_attempts'].filter(user=self.request.user)
        else:
            context['attempts'] = UserAnswerForProblemStep.objects.select_related('problem__lesson__topic__course', 'user').filter(
                problem=self.object, user=self.request.user)
        return context

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
