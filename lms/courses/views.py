from django.db.models import Prefetch
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from lms.courses.models import Course
from lms.topics.models import Topic
from lms.lessons.models import Lesson
from lms.steps.models import LessonStepConnection, Step


class CoursesList(ListView):  # Проверить, обновить
    model = Course
    template_name = 'main/courses_list.html'
    context_object_name = 'courses'

    def get_context_data(self, **kwargs):
        context = super(CoursesList, self).get_context_data(**kwargs)
        context['page_title'] = 'Список всех курсов'
        return context

    def get_queryset(self):
        return Course.objects.filter(is_outside=True, is_published=True)


class LMS_UserCoursesList(LoginRequiredMixin, ListView):  # Проверить, обновить
    model = Course
    template_name = 'lms/courses/list.html'
    context_object_name = 'courses'

    def get_context_data(self, **kwargs):
        context = super(LMS_UserCoursesList, self).get_context_data(**kwargs)
        context['page_title'] = 'Мои курсы'
        return context

    def get_queryset(self):
        return Course.objects.filter(courses_enrolls__user=self.request.user,
                                     is_published=True)


class LMS_CourseDetail(LoginRequiredMixin, DetailView):  # Проверить, обновить
    model = Course
    template_name = 'lms/courses/detail.html'
    slug_url_kwarg = 'course_slug'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super(LMS_CourseDetail, self).get_context_data(**kwargs)
        context['page_title'] = 'Курс «{}»'.format(self.object.title)
        return context

    def get_object(self):
        return get_object_or_404(
            Course.objects.prefetch_related(
                Prefetch('topics', queryset=Topic.objects.filter(
                    is_published=True).order_by('number')),
                Prefetch('topics__lessons', queryset=Lesson.objects.filter(
                    is_published=True).order_by('number')),
                Prefetch('topics__lessons__connections', queryset=LessonStepConnection.objects.filter(
                    is_published=True).order_by('number')),
            ),
            slug=self.kwargs['course_slug']
        )

    '''def get_object(self):

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
        )'''
