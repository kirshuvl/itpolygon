from cms.constructor.steps.views import CMS_StepCreate, CMS_StepDetail, CMS_StepUpdate
from cms.constructor.question_step.forms import QuestionStepCreateForm
from lms.steps.models import QuestionStep, LessonStepConnection
from lms.lessons.models import Lesson


class CMS_QuestionStepCreate(CMS_StepCreate):  # Запросов: 3
    model = QuestionStep
    form_class = QuestionStepCreateForm
    template_name = 'cms/steps/question_step/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Добавить вопрос'
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


class CMS_QuestionStepDetail(CMS_StepDetail):
    model = QuestionStep
    template_name = 'cms/steps/question_step/detail.html'


class CMS_QuestionStepUpdate(CMS_StepUpdate):
    model = QuestionStep
    form_class = QuestionStepCreateForm
    template_name = 'cms/steps/question_step/update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Редактировать вопрос: {}'.format(
            self.object.title)
        return context
    
    def form_valid(self, form):
        connect = LessonStepConnection.objects.get(lesson__slug=self.kwargs['lesson_slug'], step__slug=self.kwargs['step_slug'])
        connect.num_attempts = form.instance.num_attempts
        connect.save()

        return super().form_valid(form)
