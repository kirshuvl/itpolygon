from django.urls import reverse
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView, TemplateView
from lms.courses.models import Course
from lms.topics.models import Topic
from lms.lessons.models import Lesson
from lms.steps.models import Step, TextStep, VideoStep, QuestionStep
from lms.problems.models import ProblemStep

from cms.other.forms import \
    CourseCreateForm, \
    TopicCreateForm, \
    LessonCreateForm, \
    TextStepCreateForm, VideoStepCreateForm, QuestionStepCreateForm, ProblemStepCreateForm


class CMS_Dashboard(TemplateView):
    template_name = 'cms/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(CMS_Dashboard, self).get_context_data(**kwargs)
        context['page_title'] = 'CMS Dashboard'

        return context


class CMS_CoursesList(ListView):
    model = Course
    template_name = 'cms/courses/courses_list.html'
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
    template_name = 'cms/courses/courses_list.html'
    context_object_name = 'courses'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Все курсы на платформе'
        return context

    def get_queryset(self):
        user = self.request.user
        return Course.objects.filter(authors=user)


class CMS_CourseDetail(DetailView):
    model = Course
    template_name = 'cms/courses/course_detail.html'
    slug_url_kwarg = 'course_slug'
    context_object_name = 'course'


class CMS_CourseCreate(CreateView):
    model = Course
    form_class = CourseCreateForm
    template_name = 'cms/courses/course_create_or_update.html'

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


class CMS_CourseUpdate(UpdateView):
    model = Course
    form_class = CourseCreateForm
    template_name = 'cms/courses/course_create_or_update.html'
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
    template_name = 'cms/courses/course_delete.html'
    context_object_name = 'course'
    slug_url_kwarg = 'course_slug'

    def get_context_data(self, **kwargs):
        context = super(CMS_CourseDelete, self).get_context_data(**kwargs)
        context['page_title'] = 'Удалить курс'

        return context

    def get_success_url(self):
        return reverse('CMS_UserCoursesList')


class CMS_TopicCreate(CreateView):  # Запросов: 3
    model = Topic
    form_class = TopicCreateForm
    template_name = 'cms/topics/topic_create_or_update.html'

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


class CMS_LessonCreate(CreateView):  # Запросов: 3
    model = Lesson
    form_class = LessonCreateForm
    template_name = 'cms/lessons/lesson_create_or_update.html'

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
        super().form_valid(form)
        form.instance.type = 'QZ'
        return super().form_valid(form)


class CMS_LessonContestCreate(CMS_LessonCreate):  # Запросов: 3
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Создать контест'
        return context

    def form_valid(self, form):
        super().form_valid(form)
        form.instance.type = 'CT'
        return super().form_valid(form)


class CMS_LessonDetail(DetailView):  # Запросов: 8
    model = Lesson
    template_name = 'cms/lessons/lesson_detail.html'
    slug_url_kwarg = 'lesson_slug'
    context_object_name = 'lesson'

    def get_object(self):
        return Lesson.objects.select_related('topic__course',).prefetch_related('steps').get(slug=self.kwargs['lesson_slug'])


class CMS_StepCreate(CreateView):  # Запросов: 3
    template_name = 'cms/steps/step_create_or_update.html'

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
    template_name = 'cms/steps/text_step_create_or_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Добавить текстовый шаг'
        return context


class CMS_VideoStepCreate(CMS_StepCreate):  # Запросов: 3
    model = VideoStep
    form_class = VideoStepCreateForm
    template_name = 'cms/steps/video_step_create_or_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Добавить видео'
        return context


class CMS_QuestionStepCreate(CMS_StepCreate):  # Запросов: 3
    model = QuestionStep
    form_class = QuestionStepCreateForm
    template_name = 'cms/steps/question_step_create_or_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Добавить вопрос'
        return context


class CMS_ProblemStepCreate(CMS_StepCreate):  # Запросов: 3
    model = ProblemStep
    form_class = ProblemStepCreateForm
    template_name = 'cms/steps/problem_step_create_or_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Добавить задачу на программирование'
        return context


class CMS_TextStepDetail(DetailView):
    model = TextStep
    template_name = 'cms/steps/text_step_detail.html'
    context_object_name = 'step'
    slug_url_kwarg = 'step_slug'

class CMS_VideoStepDetail(DetailView):
    model = VideoStep
    template_name = 'cms/steps/video_step_detail.html'
    context_object_name = 'step'
    slug_url_kwarg = 'step_slug'

class CMS_QuestionStepDetail(DetailView):
    model = QuestionStep
    template_name = 'cms/steps/question_step_detail.html'
    context_object_name = 'step'
    slug_url_kwarg = 'step_slug'

class CMS_ProblemStepDetail(DetailView):
    model = ProblemStep
    template_name = 'cms/steps/problem_step_detail.html'
    context_object_name = 'step'
    slug_url_kwarg = 'step_slug'