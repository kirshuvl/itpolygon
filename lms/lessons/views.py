from django.shortcuts import render
from django.views.generic import DetailView
from django.db.models import Q
from lms.lessons.models import Lesson, LessonEnroll
from lms.steps.models import Step, StepEnroll


class LessonDetail(DetailView):
    model = Lesson
    template_name = 'lms/lessons/lesson_detail.html'
    slug_url_kwarg = 'lesson_slug'
    context_object_name = 'lesson'

    def get_context_data(self, **kwargs):
        context = super(LessonDetail, self).get_context_data(**kwargs)
        context['page_title'] = self.object.title
        context = self.get_steps(context)

        return context

    def get_steps(self, context):
        context['steps'] = Step.objects.prefetch_related(
            'lesson__topic__course',
            'steps_enrolls__user',
        ).filter(
            is_published=True,
        ).filter(Q(textstep__lesson=self.object) |
                 Q(videostep__lesson=self.object) |
                 Q(questionstep__lesson=self.object),
                 ).order_by(
            'number',
        )
        return context
