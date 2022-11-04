from django.views.generic import DetailView
from lms.lessons.models import Lesson
from lms.steps.models import Step, StepEnroll
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch


class LessonDetail(DetailView):
    model = Lesson
    template_name = 'lms/lessons/lesson_detail.html'
    slug_url_kwarg = 'lesson_slug'
    context_object_name = 'lesson'

    def get_context_data(self, **kwargs):
        context = super(LessonDetail, self).get_context_data(**kwargs)
        context['page_title'] = self.object.title

        return context

    def get_object(self):
        return get_object_or_404(
            Lesson.objects.select_related('topic__course').prefetch_related(
                Prefetch('steps', queryset=Step.objects.filter(
                    is_published=True).order_by('number')),
                Prefetch('steps__steps_enrolls', queryset=StepEnroll.objects.filter(
                    user=self.request.user))
            ),
            slug=self.kwargs['lesson_slug']
        )


class LessonStatistics(DetailView):
    model = Lesson
    template_name = 'lms/lessons/lesson_statistics.html'
    slug_url_kwarg = 'lesson_slug'
    context_object_name = 'lesson'

    def get_context_data(self, **kwargs):
        context = super(LessonStatistics, self).get_context_data(**kwargs)
        context['page_title'] = 'Статистика урока: ' + self.object.title
        
        context['all_users'] = self.get_all_user()
        return context

    def get_object(self):
        return get_object_or_404(
            Lesson.objects.select_related('topic__course').prefetch_related(
                Prefetch('steps', queryset=Step.objects.filter(
                    is_published=True).order_by('number')),
                'steps__steps_enrolls__user',
            ),
            slug=self.kwargs['lesson_slug']
        )

    def get_all_user(self):
        data = []
        for step in self.object.steps.all():
            for enroll in step.steps_enrolls.all():
                if enroll.user not in data:
                    data.append(enroll.user)
        
        return data
