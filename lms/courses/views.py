from itertools import tee
from django.views.generic import ListView, DetailView
from lms.courses.models import Course
from django.shortcuts import get_object_or_404


class CoursesList(ListView):
    model = Course
    template_name = 'lms/courses/courses_list.html'
    context_object_name = 'courses'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CoursesList, self).get_context_data(**kwargs)
        context['page_title'] = 'Список всех курсов'
        return context

    def get_queryset(self):
        return Course.objects.filter(is_published=True)


class UserCoursesList(ListView):
    model = Course
    template_name = 'lms/courses/user_courses_list.html'
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
    template_name = 'lms/courses/course_detail.html'
    slug_url_kwarg = 'course_slug'
    context_object_name = 'course'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CourseDetail, self).get_context_data(**kwargs)
        context['page_title'] = self.object.title
        return context

    def get_object(self):
        return get_object_or_404(Course.objects.prefetch_related(
            'topics__topics_enrolls__user',
            'topics__lessons__lessons_enrolls__user'),
            slug=self.kwargs['course_slug'])
