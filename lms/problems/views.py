
from lms.problems.models import ProblemStep, TestForProblemStep, UserAnswerForProblemStep
from django.views.generic import DetailView, CreateView
from lms.steps.mixins import BaseStepMixin
from lms.problems.forms import ProblemUpload
from django.shortcuts import get_object_or_404
from lms.steps.models import Step
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse
class LMS_ProblemStepDetail(BaseStepMixin, CreateView):
    template_name = 'lms/steps/problem_step/detail.html'
    form_class = ProblemUpload

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['tests'] = self.get_tests()
        context['user_attempts'] = self.get_user_attempts()
        context['all_attempts'] = self.get_all_attempts()

        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.problem = ProblemStep.objects.get(
            slug=self.kwargs['step_slug'])

        return super().form_valid(form)

    def get_tests(self):
        queryset = TestForProblemStep.objects.filter(number__lte=self.object.get_last_sample(),
                                                     number__gte=self.object.get_first_sample(),
                                                     problem=self.object.get_problem()).order_by('number')

        return queryset

    def get_all_attempts(self):
        if self.request.user == self.object.author:
            return UserAnswerForProblemStep.objects.filter(problem=self.object.get_problem()).select_related('user', 'problem')

        return None

    def get_user_attempts(self):

        return UserAnswerForProblemStep.objects.filter(user=self.request.user, problem=self.object.get_problem()).select_related('user', 'problem')

    def get_success_url(self):
        return reverse(
            "LMS_ProblemStepDetail",
            kwargs={
                'course_slug': self.kwargs['course_slug'],
                'topic_slug': self.kwargs['topic_slug'],
                'lesson_slug': self.kwargs['lesson_slug'],
                'step_slug': self.kwargs['step_slug'],
            },
        )


class LMS_UserCodeDetail(LoginRequiredMixin, DetailView):
    model = UserAnswerForProblemStep
    template_name = 'lms/problems/user_answer_detail.html'
    pk_url_kwarg = 'user_answer_pk'
    context_object_name = 'user_answer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Посылка № ' + str(self.object.pk)
        return context
