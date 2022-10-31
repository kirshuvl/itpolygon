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
        context['page_title'] = 'Статистика урока:' + self.object.title
        context = self.get_steps(context)
        # context['all_users'] = [
        #    enroll.user for enroll in LessonEnroll.objects.filter(lesson=self.object)]
        return context

    def get_steps(self, context):
        context['steps'] = Step.objects.prefetch_related(
            'lesson__topic__course',
            'steps_enrolls__user',
        ).filter(
            is_published=True,
        ).filter(lesson=self.object,
                 ).order_by(
            'number',
        )
        return context
