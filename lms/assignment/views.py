from django.views.generic import CreateView
from lms.assignment.forms import UserAnswerForAssignmentStepForm
from lms.assignment.models import AssignmentStep, UserAnswerForAssignmentStep
from lms.steps.models import Step, StepEnroll, LessonStepConnection
from django.db.models import Prefetch
from lms.steps.mixins import BaseStepMixin


class LMS_AssignmentStepDetail(BaseStepMixin, CreateView):
    template_name = 'lms/steps/assignment_step/detail.html'
    form_class = UserAnswerForAssignmentStepForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_attempts'] = UserAnswerForAssignmentStep.objects.select_related('user').filter(
            user=self.request.user, assignment=context['step'])
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.user_answer = form.cleaned_data['user_answer']
        form.instance.assignment = AssignmentStep.objects.get(
            slug=self.kwargs['step_slug'])
        form.instance.file = form.cleaned_data['file']

        return super().form_valid(form)

    def get_success_url(self):
        return self.object.assignment.get_lms_detail_url()
