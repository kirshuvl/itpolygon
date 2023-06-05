from cms.constructor.steps.views import CMS_StepCreate, CMS_StepDetail, CMS_StepUpdate, CMS_StepDelete, CMS_StepFromLibrary
from cms.constructor.text_step.forms import TextStepCreateForm
from lms.steps.models import TextStep


class CMS_TextStepCreate(CMS_StepCreate):  # Запросов: 3
    model = TextStep
    form_class = TextStepCreateForm
    template_name = 'cms/steps/text_step/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Добавить текстовый шаг'
        return context


class CMS_TextStepDetail(CMS_StepDetail):
    model = TextStep
    template_name = 'cms/steps/text_step/detail.html'


class CMS_TextStepUpdate(CMS_StepUpdate):
    model = TextStep
    form_class = TextStepCreateForm
    template_name = 'cms/steps/text_step/update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Редактировать текстовый шаг'
        return context


class CMS_TextStepDelete(CMS_StepDelete):
    model = TextStep


class CMS_TextStepFromLibrary(CMS_StepFromLibrary):
    model = TextStep
