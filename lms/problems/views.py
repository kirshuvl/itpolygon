
from lms.problems.models import ProblemStep, TestForProblemStep, UserAnswerForProblemStep
from django.views.generic import DetailView, CreateView
from lms.steps.mixins import BaseStepMixin
from lms.problems.forms import ProblemUpload
from django.shortcuts import get_object_or_404
from lms.steps.models import Step

class LMS_ProblemStepDetail(BaseStepMixin, CreateView):
    template_name = 'lms/problems/detail.html'
    form_class = ProblemUpload

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['tests'] = TestForProblemStep.objects.filter(number__lte=self.object.problemstep.last_sample,
                                                             number__gte=self.object.problemstep.first_sample,
                                                             problem=self.object.problemstep).order_by('number')
        
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

        return super(LMS_ProblemStepDetail, self).form_valid(form)


class UserCodeDetail(DetailView):
    model = UserAnswerForProblemStep
    template_name = 'lms/problems/user_answer_detail.html'
    pk_url_kwarg = 'user_answer_pk'
    context_object_name = 'user_answer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Посылка № ' + str(self.object.pk)
        return context
