from cms.constructor.steps.views import CMS_StepCreate, CMS_StepDetail, CMS_StepUpdate
from cms.constructor.video_step.forms import VideoStepCreateForm
from lms.steps.models import VideoStep


class CMS_VideoStepCreate(CMS_StepCreate):  # Запросов: 3
    model = VideoStep
    form_class = VideoStepCreateForm
    template_name = 'cms/steps/video_step/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Добавить видео шаг'
        return context


class CMS_VideoStepDetail(CMS_StepDetail):
    model = VideoStep
    template_name = 'cms/steps/video_step/detail.html'


class CMS_VideoStepUpdate(CMS_StepUpdate):
    model = VideoStep
    form_class = VideoStepCreateForm
    template_name = 'cms/steps/video_step/update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Редактировать видео шаг: {}'.format(
            self.object.title)
        return context
