from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView, TemplateView, FormView
from lms.courses.models import Course
from lms.topics.models import Topic
from lms.lessons.models import Lesson
from lms.steps.models import Step, StepEnroll, TextStep, VideoStep, QuestionStep, LessonStepConnection

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


from lms.lessons.models import Lesson
from lms.steps.models import Step, StepEnroll, TextStep, VideoStep, QuestionStep
from lms.problems.models import ProblemStep, TestForProblemStep, TestUserAnswer, UserAnswerForProblemStep
from lms.assignment.models import AssignmentStep, UserAnswerForAssignmentStep
from cms.course_builder.forms.forms import \
    TestForProblemStepForm, \
    VideoStepCreateForm, QuestionStepCreateForm, ProblemStepCreateForm, AssignmentStepCreateForm

from cms.course_builder.forms.steps.text_step import TextStepCreateForm
from lms.problems.tasks import run_user_code
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class CMS_StepCreate(CreateView):  # Запросов: 3
    template_name = 'cms/steps/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lesson'] = Lesson.objects.select_related(
            'topic__course').get(slug=self.kwargs['lesson_slug'])
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        self.object = form.save()
        self.create_connect(form)

        return super().form_valid(form)

    def create_connect(self, form):

        connect = LessonStepConnection(
            number=LessonStepConnection.objects.filter(
                lesson__slug=self.kwargs['lesson_slug']).count() + 1,
            author=self.request.user,
            lesson=Lesson.objects.get(slug=self.kwargs['lesson_slug']),
            step=self.object,
            is_published=form.instance.is_published,
        )
        connect.save()

    def get_success_url(self):
        return reverse(
            'CMS_LessonDetail',
            kwargs={
                'course_slug': self.kwargs['course_slug'],
                'topic_slug': self.kwargs['topic_slug'],
                'lesson_slug': self.kwargs['lesson_slug'],
            },
        )


class CMS_TextStepCreate(CMS_StepCreate):  # Запросов: 3
    model = TextStep
    form_class = TextStepCreateForm
    template_name = 'cms/steps/text_step/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Добавить текстовый шаг'
        return context


class CMS_VideoStepCreate(CMS_StepCreate):  # Запросов: 3
    model = VideoStep
    form_class = VideoStepCreateForm
    template_name = 'cms/steps/video_step/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Добавить видео шаг'
        return context


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


class CMS_ProblemStepCreate(CMS_StepCreate):  # Запросов: 3
    model = ProblemStep
    form_class = ProblemStepCreateForm
    template_name = 'cms/steps/problem_step/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Добавить задачу на программирование'
        return context


class CMS_AssignmentStepCreate(CMS_StepCreate):
    model = AssignmentStep
    form_class = AssignmentStepCreateForm
    template_name = 'cms/steps/assignment_step/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Добавить задание'
        return context


class CMS_StepDetail(DetailView):
    context_object_name = 'step'
    slug_url_kwarg = 'step_slug'


class CMS_TextStepDetail(CMS_StepDetail):
    model = TextStep
    template_name = 'cms/steps/text_step/detail.html'


class CMS_VideoStepDetail(CMS_StepDetail):
    model = VideoStep
    template_name = 'cms/steps/video_step/detail.html'


class CMS_QuestionStepDetail(CMS_StepDetail):
    model = QuestionStep
    template_name = 'cms/steps/question_step/detail.html'


class CMS_ProblemStepDetail(CMS_StepDetail):
    model = ProblemStep
    template_name = 'cms/steps/problem_step/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tests'] = TestForProblemStep.objects.filter(number__gte=self.object.first_test,
                                                             problem=self.object).order_by('number')
        context['samples'] = TestForProblemStep.objects.filter(number__lte=self.object.last_sample,
                                                               number__gte=self.object.first_sample,
                                                               problem=self.object).order_by('number')
        return context


class CMS_AssignmentSteppDetail(CMS_StepDetail):
    model = AssignmentStep
    template_name = 'cms/steps/assignment_step/detail.html'


class CMS_StepUpdate(UpdateView):
    context_object_name = 'step'
    slug_url_kwarg = 'step_slug'

    def get_success_url(self) -> str:
        return reverse(
            'CMS_LessonDetail',
            kwargs={
                'course_slug': self.kwargs['course_slug'],
                'topic_slug': self.kwargs['topic_slug'],
                'lesson_slug': self.kwargs['lesson_slug'],
            },
        )


class CMS_TextStepUpdate(CMS_StepUpdate):
    model = TextStep
    form_class = TextStepCreateForm
    template_name = 'cms/steps/text_step/update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Редактировать текстовый шаг: {}'.format(
            self.object.title)
        return context


class CMS_VideoStepUpdate(CMS_StepUpdate):
    model = VideoStep
    form_class = VideoStepCreateForm
    template_name = 'cms/steps/video_step/update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Редактировать видео шаг: {}'.format(
            self.object.title)
        return context


class CMS_QuestionStepUpdate(CMS_StepUpdate):
    model = QuestionStep
    form_class = QuestionStepCreateForm
    template_name = 'cms/steps/question_step/update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Редактировать вопрос: {}'.format(
            self.object.title)
        return context


class CMS_ProblemStepUpdate(CMS_StepUpdate):
    model = ProblemStep
    form_class = ProblemStepCreateForm
    template_name = 'cms/steps/problem_step/update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Редактировать задачу на программирование: {}'.format(
            self.object.title)
        return context


class CMS_AssignmentStepUpdate(CMS_StepUpdate):
    model = AssignmentStep
    form_class = AssignmentStepCreateForm
    template_name = 'cms/steps/assignment_step/update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Редактировать задание: {}'.format(
            self.object.title)
        return context


class CMS_StepDelete(DeleteView):
    model = Step
    template_name = 'cms/steps/delete.html'
    context_object_name = 'step'
    slug_url_kwarg = 'step_slug'

    def get_context_data(self, **kwargs):
        context = super(CMS_StepDelete, self).get_context_data(**kwargs)
        context['page_title'] = 'Удалить шаг'
        return context

    def get_success_url(self):
        return reverse(
            'CMS_LessonDetail',
            kwargs={
                'course_slug': self.kwargs['course_slug'],
                'topic_slug': self.kwargs['topic_slug'],
                'lesson_slug': self.kwargs['lesson_slug'],
            },
        )


class CMS_ProblemStepCreateTests(FormView):
    model = TestForProblemStep
    template_name = 'cms/steps/problem_step/create_tests.html'
    form_class = TestForProblemStepForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['step'] = ProblemStep.objects.get(
            slug=self.kwargs['step_slug'])
        return context

    def form_valid(self, form):
        zip_file = form.cleaned_data.get('zip_file')
        rewrite = form.cleaned_data.get('rewrite')
        problem = ProblemStep.objects.get(slug=self.kwargs['step_slug'])
        tests = TestForProblemStep.objects.filter(
            problem=problem).order_by('number')

        if rewrite:
            data_create = []
            if len(zip_file) <= len(tests):
                for num, test in zip_file.items():
                    tests[num - 1].input = test['input']
                    tests[num - 1].output = test['output']
            else:
                for num in range(len(tests)):
                    tests[num].input = zip_file[num + 1]['input']
                    tests[num].output = zip_file[num + 1]['output']

                for num in range(len(tests) + 1, len(zip_file) + 1, 1):
                    data_create.append(
                        TestForProblemStep(
                            input=zip_file[num]['input'],
                            output=zip_file[num]['output'],
                            problem=problem,
                            number=num
                        )

                    )
            TestForProblemStep.objects.bulk_update(tests, ['input', 'output'])
        else:
            data_create = []
            for num in zip_file:
                data_create.append(
                    TestForProblemStep(
                        input=zip_file[num]['input'],
                        output=zip_file[num]['output'],
                        problem=problem,
                        number=num + tests.count()
                    )
                )
        TestForProblemStep.objects.bulk_create(data_create)

        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse(
            'CMS_ProblemStepDetail',
            kwargs={
                'course_slug': self.kwargs['course_slug'],
                'topic_slug': self.kwargs['topic_slug'],
                'lesson_slug': self.kwargs['lesson_slug'],
                'step_slug': self.kwargs['step_slug'],
            },
        )


def connect_up(request, lesson_slug, pk):
    connections = LessonStepConnection.objects.filter(lesson__slug=lesson_slug)
    current_connection = connections.get(pk=pk)
    if current_connection.number > 1:
        previous_step = connections.get(number=current_connection.number - 1)
        current_connection.number -= 1
        previous_step.number += 1
        current_connection.save()
        previous_step.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def connect_down(request, lesson_slug, pk):
    connections = LessonStepConnection.objects.filter(lesson__slug=lesson_slug)
    current_connection = connections.get(pk=pk)
    if current_connection.number < connections.count():
        next_step = connections.get(number=current_connection.number + 1)
        current_connection.number += 1
        next_step.number -= 1
        current_connection.save()
        next_step.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def connect_sort(request, lesson_slug):
    connections = LessonStepConnection.objects.filter(
        lesson__slug=lesson_slug).order_by('number')
    for num, step in enumerate(connections):
        step.number = num + 1
        step.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
