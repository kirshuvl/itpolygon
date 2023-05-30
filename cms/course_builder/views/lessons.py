from typing import Any, Dict
from django.urls import reverse
from cms.course_builder.forms.lessons import LessonCreateForm
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from lms.topics.models import Topic
from lms.lessons.models import Lesson
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from lms.steps.models import Step, LessonStepConnection, StepEnroll
from django.db.models import Prefetch

class CMS_LessonCreate(LoginRequiredMixin, CreateView):  # Запросов: 3
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


class CMS_LessonDetail(LoginRequiredMixin, DetailView):  # Запросов: 8
    model = Lesson
    template_name = 'cms/lessons/detail.html'
    slug_url_kwarg = 'lesson_slug'
    context_object_name = 'lesson'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['connections'] = self.get_queryset()
        return context

    def get_queryset(self):
        queryset = LessonStepConnection.objects.filter(lesson=self.object).select_related('author', 'step__author').order_by('number')
        
        return queryset

    def get_object(self):
        return get_object_or_404(Lesson.objects.select_related('topic__course',), slug=self.kwargs['lesson_slug'])


class CMS_LessonUpdate(LoginRequiredMixin, UpdateView):
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


class CMS_LessonDelete(LoginRequiredMixin, DeleteView):
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


def lessons_sort(request, topic_slug):
    lessons = Lesson.objects.filter(
        topic__slug=topic_slug).order_by('number')
    for num, lesson in enumerate(lessons):
        lesson.number = num + 1
        lesson.save()

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


def lesson_check_publish(request, lesson_slug):
    lesson: Lesson = Lesson.objects.get(slug=lesson_slug)
    if lesson.is_published:
        lesson.is_published = False
    else:
        lesson.is_published = True
    lesson.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])
