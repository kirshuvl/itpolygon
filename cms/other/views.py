from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView, TemplateView, FormView
from lms.courses.models import Course
from lms.topics.models import Topic
from lms.lessons.models import Lesson
from lms.steps.models import Step, StepEnroll, TextStep, VideoStep, QuestionStep
from lms.problems.models import ProblemStep, TestForProblemStep, TestUserAnswer, UserAnswerForProblemStep
from lms.assignment.models import AssignmentStep, UserAnswerForAssignmentStep
from users.models import CustomUser
from cms.other.forms import \
    CourseCreateForm, \
    TestForProblemStepForm, \
    TopicCreateForm, \
    LessonCreateForm, \
    TextStepCreateForm, VideoStepCreateForm, QuestionStepCreateForm, ProblemStepCreateForm, AssignmentStepCreateForm
from lms.problems.tasks import run_user_code


class CMS_Dashboard(TemplateView):
    template_name = 'cms/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(CMS_Dashboard, self).get_context_data(**kwargs)
        context['page_title'] = 'CMS Dashboard'

        return context


class CMS_CoursesList(ListView):
    model = Course
    template_name = 'cms/courses/list.html'
    context_object_name = 'courses'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Все курсы на платформе'
        return context

    def get_queryset(self):
        user = self.request.user
        return Course.objects.all()


class CMS_UserCoursesList(ListView):
    model = Course
    template_name = 'cms/courses/list.html'
    context_object_name = 'courses'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Мои курсы на платформе'
        return context

    def get_queryset(self):
        user = self.request.user
        return Course.objects.filter(authors=user)


class CMS_CourseCreate(CreateView):
    model = Course
    form_class = CourseCreateForm
    template_name = 'cms/courses/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Создать курс'
        return context

    def form_valid(self, form):
        form.instance.save()
        form.instance.authors.add(self.request.user.pk)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('CMS_UserCoursesList')


class CMS_CourseDetail(DetailView):
    model = Course
    template_name = 'cms/courses/detail.html'
    slug_url_kwarg = 'course_slug'
    context_object_name = 'course'

    def get_object(self):

        return get_object_or_404(
            Course.objects.prefetch_related(
                Prefetch('topics', queryset=Topic.objects.order_by('number')),
                Prefetch('topics__lessons',
                         queryset=Lesson.objects.order_by('number')),
                Prefetch('topics__lessons__steps',
                         queryset=Step.objects.order_by('number')),
            ),
            slug=self.kwargs['course_slug']
        )


class CMS_CourseUpdate(UpdateView):
    model = Course
    form_class = CourseCreateForm
    template_name = 'cms/courses/update.html'
    context_object_name = 'course'
    slug_url_kwarg = 'course_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Редактировать курс'
        return context

    def get_success_url(self):
        return reverse('CMS_UserCoursesList')


class CMS_CourseDelete(DeleteView):
    model = Course
    template_name = 'cms/courses/delete.html'
    context_object_name = 'course'
    slug_url_kwarg = 'course_slug'

    def get_context_data(self, **kwargs):
        context = super(CMS_CourseDelete, self).get_context_data(**kwargs)
        context['page_title'] = 'Удалить курс'

        return context

    def get_success_url(self):
        return reverse('CMS_UserCoursesList')


class CMS_CourseStatistics(DetailView):
    model = Course
    template_name = 'cms/courses/statistics.html'
    context_object_name = 'course'
    slug_url_kwarg = 'course_slug'

    def get_context_data(self, **kwargs):
        context = super(CMS_CourseStatistics, self).get_context_data(**kwargs)
        context['users'] = CustomUser.objects.filter(
            courses_enrolls__course=self.object).order_by('first_name')
        context['page_title'] = 'Статистика курса: ' + self.object.title

        return context

    def get_object(self):

        return get_object_or_404(
            Course.objects.prefetch_related(
                Prefetch('topics', queryset=Topic.objects.filter(
                    is_published=True).order_by('number')),
                Prefetch('topics__lessons', queryset=Lesson.objects.filter(
                    is_published=True).order_by('number')),
                Prefetch('topics__lessons__steps', queryset=Step.objects.filter(
                    is_published=True).order_by('number')),
                Prefetch('topics__lessons__steps__steps_enrolls',
                         queryset=StepEnroll.objects.select_related('user')),
            ),
            slug=self.kwargs['course_slug']
        )


class CMS_CourseSubmissions(ListView):
    model = UserAnswerForProblemStep
    template_name = 'cms/courses/problems.html'
    context_object_name = 'users_attempts'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super(CMS_CourseSubmissions, self).get_context_data(**kwargs)
        context['course'] = Course.objects.get(slug=self.kwargs['course_slug'])

        return context

    def get_queryset(self):
        return UserAnswerForProblemStep.objects.select_related('problem__lesson__topic__course', 'user').filter(problem__lesson__topic__course__slug=self.kwargs['course_slug'])


class CMS_TopicCreate(CreateView):  # Запросов: 3
    model = Topic
    form_class = TopicCreateForm
    template_name = 'cms/topics/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Создать тему урока'
        context['course'] = Course.objects.get(slug=self.kwargs['course_slug'])
        return context

    def form_valid(self, form):
        course = Course.objects.get(slug=self.kwargs['course_slug'])
        form.instance.author = self.request.user
        form.instance.number = Topic.objects.filter(course=course).count() + 1
        form.instance.course = course

        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'CMS_CourseDetail',
            kwargs={
                'course_slug': self.kwargs['course_slug'],
            },
        )


class CMS_TopicDetail(DetailView):
    model = Topic
    template_name = 'cms/topics/detail.html'
    slug_url_kwarg = 'topic_slug'
    context_object_name = 'topic'


class CMS_TopicUpdate(UpdateView):
    model = Topic
    form_class = TopicCreateForm
    template_name = 'cms/topics/update.html'
    context_object_name = 'topic'
    slug_url_kwarg = 'topic_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Редактировать урок {}'.format(
            self.object.title)

        return context

    def get_object(self):

        return get_object_or_404(Topic.objects.select_related('course'), slug=self.kwargs['topic_slug'])

    def get_success_url(self):
        return reverse(
            'CMS_CourseDetail',
            kwargs={
                'course_slug': self.kwargs['course_slug'],
            },
        )


class CMS_TopicDelete(DeleteView):
    model = Topic
    template_name = 'cms/topics/delete.html'
    context_object_name = 'topic'
    slug_url_kwarg = 'topic_slug'

    def get_object(self):

        return get_object_or_404(Topic.objects.select_related('course'), slug=self.kwargs['topic_slug'])

    def get_success_url(self):
        return reverse(
            'CMS_CourseDetail',
            kwargs={
                'course_slug': self.kwargs['course_slug'],
            },
        )


class CMS_LessonCreate(CreateView):  # Запросов: 3
    model = Lesson
    form_class = LessonCreateForm
    template_name = 'cms/lessons/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Создать урок'
        context['topic'] = Topic.objects.select_related(
            'course').get(slug=self.kwargs['topic_slug'])
        return context

    def form_valid(self, form):
        topic = Topic.objects.get(slug=self.kwargs['topic_slug'])
        form.instance.author = self.request.user
        form.instance.number = Lesson.objects.filter(topic=topic).count() + 1
        form.instance.topic = topic

        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'CMS_CourseDetail',
            kwargs={
                'course_slug': self.kwargs['course_slug'],
            },
        )


class CMS_LessonQuizCreate(CMS_LessonCreate):  # Запросов: 3
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Создать урок - тест'
        return context

    def form_valid(self, form):
        form.instance.type = 'QZ'
        return super().form_valid(form)


class CMS_LessonContestCreate(CMS_LessonCreate):  # Запросов: 3
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Создать контест'
        return context

    def form_valid(self, form):
        form.instance.type = 'CT'
        return super().form_valid(form)


class CMS_LessonDetail(DetailView):  # Запросов: 8
    model = Lesson
    template_name = 'cms/lessons/detail.html'
    slug_url_kwarg = 'lesson_slug'
    context_object_name = 'lesson'

    def get_object(self):
        return Lesson.objects.select_related('topic__course',).prefetch_related('steps').get(slug=self.kwargs['lesson_slug'])


class CMS_LessonUpdate(UpdateView):
    model = Lesson
    form_class = LessonCreateForm
    template_name = 'cms/lessons/update.html'
    slug_url_kwarg = 'lesson_slug'

    def get_success_url(self):
        return reverse(
            'CMS_CourseDetail',
            kwargs={
                'course_slug': self.kwargs['course_slug'],
            },
        )


class CMS_LessonDelete(DeleteView):
    model = Lesson
    template_name = 'cms/lessons/delete.html'
    context_object_name = 'lesson'
    slug_url_kwarg = 'lesson_slug'

    def get_context_data(self, **kwargs):
        context = super(CMS_LessonDelete, self).get_context_data(**kwargs)
        context['page_title'] = 'Удалить урок'
        return context

    def get_success_url(self):
        return reverse(
            'CMS_CourseDetail',
            kwargs={
                'course_slug': self.kwargs['course_slug'],
            },
        )


class CMS_StepCreate(CreateView):  # Запросов: 3
    template_name = 'cms/steps/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lesson'] = Lesson.objects.select_related(
            'topic__course').get(slug=self.kwargs['lesson_slug'])
        return context

    def form_valid(self, form):
        lesson = Lesson.objects.get(slug=self.kwargs['lesson_slug'])
        form.instance.number = Step.objects.filter(lesson=lesson).count() + 1
        form.instance.author = self.request.user
        form.instance.lesson = lesson

        return super().form_valid(form)

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


def course_check_publish(request, course_slug):
    course = Course.objects.get(slug=course_slug)
    if course.is_published:
        course.is_published = False
    else:
        course.is_published = True
    course.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def topic_check_publish(request, topic_slug):
    topic = Topic.objects.get(slug=topic_slug)
    if topic.is_published:
        topic.is_published = False
    else:
        topic.is_published = True
    topic.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def lesson_check_publish(request, lesson_slug):
    lesson = Lesson.objects.get(slug=lesson_slug)
    if lesson.is_published:
        lesson.is_published = False
    else:
        lesson.is_published = True
    lesson.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def step_check_publish(request, step_slug):
    step = Step.objects.get(slug=step_slug)
    if step.is_published:
        step.is_published = False
    else:
        step.is_published = True
    step.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def topic_up(request, course_slug, topic_slug):
    topics = Topic.objects.filter(course__slug=course_slug)
    topic = topics.get(slug=topic_slug)

    if topic.number > 1:
        topic_2 = topics.get(number=topic.number-1)
        topic.number -= 1
        topic_2.number += 1
        topic.save()
        topic_2.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def topic_down(request, course_slug, topic_slug):
    topics = Topic.objects.filter(course__slug=course_slug)
    topic = topics.get(slug=topic_slug)

    if topic.number < topics.count():
        topic_2 = topics.get(number=topic.number+1)
        topic.number += 1
        topic_2.number -= 1
        topic.save()
        topic_2.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def topics_sort(request, course_slug):
    topics = Topic.objects.filter(
        course__slug=course_slug).order_by('number')

    for num, topic in enumerate(topics):
        topic.number = num + 1
        topic.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def lesson_up(request, course_slug, topic_slug, lesson_slug):
    lessons = Lesson.objects.filter(topic__slug=topic_slug)
    lesson = lessons.get(slug=lesson_slug)
    if lesson.number > 1:
        lesson_2 = lessons.get(number=lesson.number - 1)
        lesson.number -= 1
        lesson_2.number += 1
        lesson.save()
        lesson_2.save()
    else:
        if lesson.topic.number > 1:
            topic = Topic.objects.get(
                course__slug=course_slug, number=lesson.topic.number - 1)
            lesson.topic = topic
            lesson.number = Lesson.objects.filter(
                topic__slug=topic.slug).count() + 1
            lesson.save()
            lessons_sort(request, topic_slug)

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def lesson_down(request, course_slug, topic_slug, lesson_slug):
    lessons = Lesson.objects.filter(topic__slug=topic_slug)
    lesson = lessons.get(slug=lesson_slug)
    if lesson.number < lessons.count():
        lesson_2 = lessons.get(number=lesson.number + 1)
        lesson.number += 1
        lesson_2.number -= 1
        lesson.save()
        lesson_2.save()
    else:
        topics = Topic.objects.filter(course__slug=course_slug)
        if lesson.topic.number < topics.count():
            topic = topics.get(slug=topic_slug)
            lesson.topic = topics.get(number=lesson.topic.number + 1)
            lesson.number = 0

            lesson.save()
            lessons_sort(request, lesson.topic.slug)

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def lessons_sort(request, topic_slug):
    lessons = Lesson.objects.filter(
        topic__slug=topic_slug).order_by('number')
    for num, lesson in enumerate(lessons):
        lesson.number = num + 1
        lesson.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def step_up(request, course_slug, topic_slug, lesson_slug, step_slug):
    steps = Step.objects.filter(lesson__slug=lesson_slug)
    current_step = steps.get(slug=step_slug)
    if current_step.number > 1:
        previous_step = steps.get(number=current_step.number - 1)
        current_step.number -= 1
        previous_step.number += 1
        current_step.save()
        previous_step.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def step_down(request, course_slug, topic_slug, lesson_slug, step_slug):
    steps = Step.objects.filter(lesson__slug=lesson_slug)
    current_step = steps.get(slug=step_slug)
    if current_step.number < steps.count():
        next_step = steps.get(number=current_step.number + 1)
        current_step.number += 1
        next_step.number -= 1
        current_step.save()
        next_step.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def steps_sort(request, lesson_slug):
    steps = Step.objects.filter(
        lesson__slug=lesson_slug).order_by('number')
    for num, step in enumerate(steps):
        step.number = num + 1
        step.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def rerun_submission(request, user_answer_pk):
    user_answer = UserAnswerForProblemStep.objects.get(pk=user_answer_pk)
    user_answer.verdict = 'PR'
    user_answer.cputime = 0
    user_answer.first_fail_test = 0
    user_answer.points = 0
    user_answer.save()
    TestUserAnswer.objects.filter(
        user=user_answer.user, code=user_answer).delete()
    run_user_code.delay(user_answer_pk)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

class CMS_UserAssignmentsList(ListView):
    model = UserAnswerForAssignmentStep
    template_name = 'cms/steps/assignment_step/list.html'
    context_object_name = 'assignments'


    def get_queryset(self):
        return UserAnswerForAssignmentStep.objects.select_related('assignment__lesson__topic__course', 'user').filter(assignment__lesson__topic__course__authors=self.request.user)