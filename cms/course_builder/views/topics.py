from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from lms.courses.models import Course
from lms.topics.models import Topic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from cms.course_builder.forms.topics import TopicCreateForm
from django.http import HttpResponseRedirect


class CMS_TopicCreate(LoginRequiredMixin, CreateView):  # Запросов: 3
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

        return self.object.course.get_cms_detail_url()


class CMS_TopicDetail(LoginRequiredMixin, DetailView):
    model = Topic
    template_name = 'cms/topics/detail.html'
    slug_url_kwarg = 'topic_slug'
    context_object_name = 'topic'


class CMS_TopicUpdate(LoginRequiredMixin, UpdateView):
    model = Topic
    form_class = TopicCreateForm
    template_name = 'cms/topics/update.html'
    context_object_name = 'topic'
    slug_url_kwarg = 'topic_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Редактировать урок'
        return context

    def get_object(self):

        return get_object_or_404(Topic.objects.select_related('course'), slug=self.kwargs['topic_slug'])

    def get_success_url(self):

        return self.object.course.get_cms_detail_url()


class CMS_TopicDelete(LoginRequiredMixin, DeleteView):
    model = Topic
    template_name = 'cms/topics/delete.html'
    context_object_name = 'topic'
    slug_url_kwarg = 'topic_slug'

    def get_object(self):

        return get_object_or_404(Topic.objects.select_related('course'), slug=self.kwargs['topic_slug'])

    def get_success_url(self):

        return self.object.course.get_cms_detail_url()


def topics_sort(request, course_slug):
    topics = Topic.objects.filter(
        course__slug=course_slug).order_by('number')

    for num, topic in enumerate(topics):
        topic.number = num + 1
        topic.save()

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


def topic_check_publish(request, topic_slug):
    topic = Topic.objects.get(slug=topic_slug)
    if topic.is_published:
        topic.is_published = False
    else:
        topic.is_published = True
    topic.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])
