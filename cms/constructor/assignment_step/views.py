from cms.constructor.steps.views import CMS_StepCreate, CMS_StepDetail, CMS_StepUpdate
from cms.constructor.assignment_step.forms import AssignmentStepCreateForm
from lms.assignment.models import AssignmentStep


class CMS_AssignmentStepCreate(CMS_StepCreate):
    model = AssignmentStep
    form_class = AssignmentStepCreateForm
    template_name = 'cms/steps/assignment_step/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Добавить задание'
        return context


class CMS_AssignmentSteppDetail(CMS_StepDetail):
    model = AssignmentStep
    template_name = 'cms/steps/assignment_step/detail.html'


class CMS_AssignmentStepUpdate(CMS_StepUpdate):
    model = AssignmentStep
    form_class = AssignmentStepCreateForm
    template_name = 'cms/steps/assignment_step/update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Редактировать задание: {}'.format(
            self.object.title)
        return context
