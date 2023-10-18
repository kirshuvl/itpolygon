from django.db.models import Prefetch
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from lms.courses.models import Course
from lms.topics.models import Topic
from lms.lessons.models import Lesson
from lms.steps.models import LessonStepConnection, StepEnroll


class CoursesList(ListView):  # Проверить, обновить
    model = Course
    template_name = 'main/courses_list.html'
    context_object_name = 'courses'

    def get_context_data(self, **kwargs):
        context = super(CoursesList, self).get_context_data(**kwargs)
        context['page_title'] = 'Список всех курсов - ИТ Полигон'
        print(context)
        return context

    def get_queryset(self):
        return Course.objects.filter(is_search=True, is_published=True)


class LMS_UserCoursesList(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'lms/courses/list.html'
    context_object_name = 'courses'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Мои курсы - ИТ Полигон'
        return context

    def get_queryset(self):
        return Course.objects.filter(courses_enrolls__user=self.request.user, is_published=True).prefetch_related(
            Prefetch('topics', queryset=Topic.objects.filter(
                is_published=True).order_by('number')),
            Prefetch('topics__lessons', queryset=Lesson.objects.filter(
                is_published=True).order_by('number')),
            Prefetch('topics__lessons__connections', queryset=LessonStepConnection.objects.filter(
                is_published=True).select_related('step').prefetch_related(
                Prefetch('step__steps_enrolls', queryset=StepEnroll.objects.filter(
                    user=self.request.user))
            ).order_by('number')),
        )


class LMS_CourseDetail(LoginRequiredMixin, DetailView):  # Проверить, обновить
    model = Course
    template_name = 'lms/courses/detail.html'
    slug_url_kwarg = 'course_slug'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'{self.object.title} - ИТ Полигон'
        return context

    def get_object(self):
        return get_object_or_404(
            Course.objects.prefetch_related(
                Prefetch('topics', queryset=Topic.objects.filter(
                    is_published=True).order_by('number')),
                Prefetch('topics__lessons', queryset=Lesson.objects.filter(
                    is_published=True).order_by('number')),
                Prefetch('topics__lessons__connections', queryset=LessonStepConnection.objects.filter(
                    is_published=True).select_related('step').prefetch_related(
                    Prefetch('step__steps_enrolls', queryset=StepEnroll.objects.filter(
                        user=self.request.user))
                ).order_by('number')),
            ),
            slug=self.kwargs['course_slug']
        )
