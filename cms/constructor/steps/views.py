from django.db import models
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView
from lms.lessons.models import Lesson
from lms.steps.models import Step, LessonStepConnection
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from lms.lessons.models import Lesson
from django.db.models import Prefetch
from cms.other.views import PermissonMixin


class CMS_StepCreate(LoginRequiredMixin, PermissonMixin, CreateView):  # Запросов: 3
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


class CMS_StepDetail(LoginRequiredMixin, PermissonMixin, DetailView):
    model = Step
    context_object_name = 'step'
    slug_url_kwarg = 'step_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lesson'] = Lesson.objects.select_related(
            'topic__course').get(slug=self.kwargs['lesson_slug'])
        return context

    def get_queryset(self):
        queryset = self.model.objects.prefetch_related(Prefetch('connections', queryset=LessonStepConnection.objects.filter(
            lesson__slug=self.kwargs['lesson_slug'])))

        return queryset


class CMS_StepUpdate(LoginRequiredMixin, PermissonMixin, UpdateView):
    model = Step
    context_object_name = 'step'
    slug_url_kwarg = 'step_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lesson'] = Lesson.objects.select_related(
            'topic__course').get(slug=self.kwargs['lesson_slug'])
        return context

    def get_queryset(self):
        queryset = self.model.objects.prefetch_related(Prefetch('connections', queryset=LessonStepConnection.objects.filter(
            lesson__slug=self.kwargs['lesson_slug'])))

        return queryset

    def get_success_url(self):
        return self.object.get_cms_detail_url()


class CMS_StepDelete(LoginRequiredMixin, PermissonMixin, DeleteView):
    model = Step
    template_name = 'cms/steps/delete.html'
    context_object_name = 'step'
    slug_url_kwarg = 'step_slug'

    def get_context_data(self, **kwargs):
        context = super(CMS_StepDelete, self).get_context_data(**kwargs)
        context['lesson'] = Lesson.objects.select_related(
            'topic__course').get(slug=self.kwargs['lesson_slug'])
        return context

    def get_queryset(self):
        queryset = self.model.objects.prefetch_related(Prefetch('connections', queryset=LessonStepConnection.objects.filter(
            lesson__slug=self.kwargs['lesson_slug'])))

        return queryset

    def get_success_url(self):
        lesson: Lesson = Lesson.objects.get(slug=self.kwargs['lesson_slug'])
        return reverse(
            'CMS_LessonDetail',
            kwargs={
                'course_slug': lesson.topic.course.slug,
                'topic_slug': lesson.topic.slug,
                'lesson_slug': lesson.slug,
            },
        )


class CMS_StepFromLibrary(LoginRequiredMixin, PermissonMixin, ListView):
    model = Step
    context_object_name = 'steps'
    template_name = 'cms/steps/library.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lesson'] = Lesson.objects.select_related(
            'topic__course').get(slug=self.kwargs['lesson_slug'])
        context['page_title'] = 'Добавить из библиотеки'
        return context

    def get_queryset(self):
        return super().get_queryset().exclude(connections__lesson__slug=self.kwargs['lesson_slug'])


def connect_create(request, course_slug, topic_slug, lesson_slug, step_slug):
    connect = LessonStepConnection(
        number=LessonStepConnection.objects.filter(
            lesson__slug=lesson_slug).count() + 1,
        author=request.user,
        lesson=Lesson.objects.get(slug=lesson_slug),
        step=Step.objects.get(slug=step_slug),
    )
    connect.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def connect_delete(request, course_slug, topic_slug, lesson_slug, step_slug):
    connect = LessonStepConnection.objects.get(
        lesson__slug=lesson_slug, step__slug=step_slug)
    connect.delete()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def connect_up(request, course_slug, topic_slug, lesson_slug, step_slug):
    connections = LessonStepConnection.objects.filter(lesson__slug=lesson_slug)
    current_connection = connections.get(step__slug=step_slug)
    if current_connection.number > 1:
        previous_step = connections.get(number=current_connection.number - 1)
        current_connection.number -= 1
        previous_step.number += 1
        current_connection.save()
        previous_step.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def connect_down(request, course_slug, topic_slug, lesson_slug, step_slug):
    connections = LessonStepConnection.objects.filter(lesson__slug=lesson_slug)
    current_connection = connections.get(step__slug=step_slug)
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


def connect_check_publish(request, course_slug, topic_slug, lesson_slug, step_slug):
    connect: LessonStepConnection = LessonStepConnection.objects.select_related(
        'step__author').get(lesson__slug=lesson_slug, step__slug=step_slug)
    step = connect.step
    if connect.is_published:
        connect.is_published = False
        if step.author == request.user:
            step.is_published = False
    else:
        connect.is_published = True
        if step.author == request.user:
            step.is_published = True
    connect.save()
    step.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])
