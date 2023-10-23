from django.db import models
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView
from lms.courses.models import Course
from lms.topics.models import Topic
from lms.lessons.models import Lesson
from lms.steps.models import Step, LessonStepConnection
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from cms.other.views import PermissonMixin

from cms.constructor.lessons.forms import LessonCreateForm


class CMS_LessonCreate(LoginRequiredMixin, PermissonMixin, CreateView):  # Запросов: 3
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


class CMS_LessonDetail(LoginRequiredMixin, PermissonMixin, DetailView):  # Запросов: 8
    model = Lesson
    template_name = 'cms/lessons/detail.html'
    slug_url_kwarg = 'lesson_slug'
    context_object_name = 'lesson'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['steps'] = self.get_queryset()
        return context

    def get_queryset(self):
        queryset = Step.objects.select_related('author').\
            prefetch_related(
            Prefetch('connections', queryset=LessonStepConnection.objects.filter(
                lesson__slug=self.kwargs['lesson_slug']).select_related('author'))).filter(connections__lesson__slug=self.kwargs['lesson_slug']).order_by('connections__number')
        return queryset

    '''def get_queryset2(self):
        queryset = Step.objects.\
            filter(connections__lesson__slug=self.kwargs['lesson_slug'], connections__is_published=True).select_related('author').\
            prefetch_related(
                Prefetch('connections', queryset=LessonStepConnection.objects.filter(
                    lesson__slug=self.kwargs['lesson_slug'])),
                Prefetch('steps_enrolls',
                         queryset=StepEnroll.objects.select_related('user').filter(user=self.request.user))).order_by('connections__number')
        
        return queryset'''

    def get_object(self):
        return get_object_or_404(Lesson.objects.select_related('topic__course',), slug=self.kwargs['lesson_slug'])


class CMS_LessonUpdate(LoginRequiredMixin, PermissonMixin, UpdateView):
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


class CMS_LessonDelete(LoginRequiredMixin, PermissonMixin, DeleteView):
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


def lesson_up(request, course_slug, topic_slug, lesson_slug):  # Rewrite
    lessons = Lesson.objects.filter(topic__slug=topic_slug)
    lesson: Lesson = lessons.get(slug=lesson_slug)
    if lesson.number > 1:
        lesson_2 = lessons.get(number=lesson.number - 1)
        lesson.number -= 1
        lesson_2.number += 1
        lesson.save()
        lesson_2.save()
    else:
        if lesson.topic.number > 1:
            q = lesson.topic
            topic: Topic = Topic.objects.get(
                course__slug=course_slug, number=lesson.topic.number - 1)
            lesson.topic = topic
            lesson.number = Lesson.objects.filter(
                topic__slug=topic.slug).count() + 1
            lesson.save()
            lessons_sort(request, lesson.topic.course.slug, lesson.topic.slug)
            lessons_sort(request, q.course.slug, q.slug)

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def lesson_down(request, course_slug, topic_slug, lesson_slug):  # Rewrite
    lessons = Lesson.objects.filter(topic__slug=topic_slug)
    lesson: Lesson = lessons.get(slug=lesson_slug)
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
            lessons_sort(request, lesson.topic.course.slug, lesson.topic.slug)

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def lesson_check_publish(request, lesson_slug):  # Rewrite
    lesson: Lesson = Lesson.objects.get(slug=lesson_slug)
    if lesson.is_published:
        lesson.is_published = False
    else:
        lesson.is_published = True
    lesson.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def lessons_sort(request, course_slug, topic_slug):  # Rewrite
    lessons = Lesson.objects.filter(
        topic__slug=topic_slug).order_by('number')
    for num, lesson in enumerate(lessons):
        lesson.number = num + 1
        lesson.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])
