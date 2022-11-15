from django.views.generic import CreateView
from lms.assignment.forms import UserAnswerForAssignmentStepForm
from lms.assignment.models import AssignmentStep, UserAnswerForAssignmentStep
from lms.steps.models import Step, StepEnroll
from django.db.models import Prefetch


class AssignmentStepDetail(CreateView):
    template_name = 'lms/steps/assignment_detail.html'
    form_class = UserAnswerForAssignmentStepForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['steps'] = self.get_queryset()
        context['step'] = context['steps'].get(slug=self.kwargs['step_slug'])
        context['attempts'] = UserAnswerForAssignmentStep.objects.select_related('user').filter(
            user=self.request.user, assignment=context['step'])

        StepEnroll.objects.get_or_create(
            step=context['step'],
            user=self.request.user
        )
        return context

    def get_queryset(self):
        self.queryset = Step.objects.select_related('lesson__topic__course').\
            prefetch_related(
                Prefetch('steps_enrolls', queryset=StepEnroll.objects.filter(
                    user=self.request.user))
        ).filter(lesson__slug=self.kwargs['lesson_slug'], is_published=True).order_by('number')
        return self.queryset

    def form_valid(self, form):
        form.instance.user_answer = form.cleaned_data['user_answer']
        form.instance.file = form.cleaned_data['file']
        form.instance.user = self.request.user
        form.instance.assignment = AssignmentStep.objects.get(
            slug=self.kwargs['step_slug'])

        return super().form_valid(form)
