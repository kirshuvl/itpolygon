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


from cms.constructor.courses.forms import CourseCreateForm


class CMS_CourseCreate(LoginRequiredMixin, PermissonMixin, CreateView):
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
        return reverse('CMS_CoursesList')


class CMS_CourseDetail(LoginRequiredMixin, PermissonMixin, DetailView):
    model = Course
    template_name = 'cms/courses/detail.html'
    slug_url_kwarg = 'course_slug'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Просмотр курса'
        return context

    def get_object(self):

        return get_object_or_404(
            Course.objects.prefetch_related(
                Prefetch('topics', queryset=Topic.objects.order_by('number')),
                Prefetch('topics__lessons',
                         queryset=Lesson.objects.order_by('number')),
                Prefetch('topics__lessons__connections',
                         queryset=LessonStepConnection.objects.order_by('number')),
            ),
            slug=self.kwargs['course_slug']
        )


class CMS_CourseUpdate(LoginRequiredMixin, PermissonMixin, UpdateView):
    model = Course
    form_class = CourseCreateForm
    template_name = 'cms/courses/update.html'
    slug_url_kwarg = 'course_slug'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Редактировать курс'
        return context

    def get_success_url(self):
        return self.get_object().get_cms_detail_url()


class CMS_CourseDelete(LoginRequiredMixin, PermissonMixin, DeleteView):
    model = Course
    template_name = 'cms/courses/delete.html'
    slug_url_kwarg = 'course_slug'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super(CMS_CourseDelete, self).get_context_data(**kwargs)
        context['page_title'] = 'Удалить курс'

        return context

    def get_success_url(self):
        return reverse('CMS_CoursesList')


class CMS_CoursesList(LoginRequiredMixin, PermissonMixin, ListView):
    model = Course
    template_name = 'cms/courses/list.html'
    context_object_name = 'courses'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Мои курсы на платформе'
        return context

    def get_queryset(self):

        return Course.objects.filter(authors=self.request.user)
