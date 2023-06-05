from cms.constructor.steps.views import CMS_StepCreate, CMS_StepDetail, CMS_StepUpdate
from cms.constructor.question_choice_step.forms import QuestionChoiceStepCreateForm
from lms.steps.models import QuestionChoiceStep, LessonStepConnection
from lms.lessons.models import Lesson


class CMS_QuestionChoiceStepCreate(CMS_StepCreate):
    model = QuestionChoiceStep
    form_class = QuestionChoiceStepCreateForm
    template_name = 'cms/steps/question_choice_step/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Добавить вопрос c выбором ответа'
        return context

    def create_connect(self, form):

        connect = LessonStepConnection(
            number=LessonStepConnection.objects.filter(
                lesson__slug=self.kwargs['lesson_slug']).count() + 1,
            author=self.request.user,
            lesson=Lesson.objects.get(slug=self.kwargs['lesson_slug']),
            step=self.object,
            is_published=form.instance.is_published,
            num_attempts=form.instance.num_attempts
        )
        connect.save()

    def get_success_url(self):
        return self.object.get_cms_detail_url()


class CMS_QuestionChoiceStepDetail(CMS_StepDetail):
    model = QuestionChoiceStep
    template_name = 'cms/steps/question_choice_step/detail.html'


class CMS_QuestionChoiceStepUpdate(CMS_StepUpdate):
    model = QuestionChoiceStep
    form_class = QuestionChoiceStepCreateForm
    template_name = 'cms/steps/question_choice_step/update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Редактировать вопрос: {}'.format(
            self.object.title)
        return context

    def form_valid(self, form):
        connect = LessonStepConnection.objects.get(
            lesson__slug=self.kwargs['lesson_slug'], step__slug=self.kwargs['step_slug'])
        connect.num_attempts = form.instance.num_attempts
        connect.save()

        return super().form_valid(form)
