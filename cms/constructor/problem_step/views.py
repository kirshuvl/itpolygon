from django.urls import reverse
from django.views.generic import FormView
from cms.constructor.steps.views import CMS_StepCreate, CMS_StepDetail, CMS_StepUpdate
from cms.constructor.problem_step.forms import ProblemStepCreateForm, TestForProblemStepForm
from lms.problems.models import ProblemStep, TestForProblemStep
from lms.lessons.models import Lesson




class CMS_ProblemStepCreate(CMS_StepCreate):  # Запросов: 3
    model = ProblemStep
    form_class = ProblemStepCreateForm
    template_name = 'cms/steps/problem_step/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Добавить задачу на программирование'
        return context
    



class CMS_ProblemStepDetail(CMS_StepDetail):
    model = ProblemStep
    template_name = 'cms/steps/problem_step/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tests'] = self.get_tests()
        context['samples'] = self.get_samples()
        return context
    
    def get_tests(self):
        queryset = TestForProblemStep.objects.filter(number__gte=self.object.get_first_test(),
                                                     problem=self.object.get_problem()).order_by('number')

        return queryset
    
    def get_samples(self):
        queryset = TestForProblemStep.objects.filter(number__lte=self.object.get_last_sample(),
                                                     number__gte=self.object.get_first_sample(),
                                                     problem=self.object.get_problem()).order_by('number')

        return queryset
    



class CMS_ProblemStepUpdate(CMS_StepUpdate):
    model = ProblemStep
    form_class = ProblemStepCreateForm
    template_name = 'cms/steps/problem_step/update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Редактировать задачу на программирование: {}'.format(
            self.object.title)
        return context
    


class CMS_ProblemStepCreateTests(FormView):
    model = TestForProblemStep
    template_name = 'cms/steps/problem_step/create_tests.html'
    form_class = TestForProblemStepForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['step'] = ProblemStep.objects.get(
            slug=self.kwargs['step_slug'])
        context['lesson'] = Lesson.objects.select_related(
            'topic__course').get(slug=self.kwargs['lesson_slug'])
        
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
