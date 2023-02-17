from itertools import tee
from django.views.generic import ListView, DetailView
from lms.courses.models import Course
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from lms.lessons.models import Lesson
from lms.steps.models import Step, StepEnroll
from lms.topics.models import Topic
from django.contrib.auth.mixins import LoginRequiredMixin

class CoursesList(ListView):
    model = Course
    template_name = 'main/courses_list.html'
    context_object_name = 'courses'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CoursesList, self).get_context_data(**kwargs)
        context['page_title'] = 'Список всех курсов'
        return context

    def get_queryset(self):
        return Course.objects.filter(is_published=True)


class UserCoursesList(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'lms/courses/list.html'
    context_object_name = 'courses'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserCoursesList, self).get_context_data(**kwargs)
        context['page_title'] = 'Мои курсы'
        return context

    def get_queryset(self):
        return Course.objects.filter(courses_enrolls__user=self.request.user,
                                     is_published=True)


class CourseDetail(DetailView):
    model = Course
    template_name = 'lms/courses/detail.html'
    slug_url_kwarg = 'course_slug'
    context_object_name = 'course'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CourseDetail, self).get_context_data(**kwargs)
        context['page_title'] = 'Курс «{}»'.format(self.object.title)
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
                         queryset=StepEnroll.objects.filter(user=self.request.user)),
            ),
            slug=self.kwargs['course_slug']
        )
