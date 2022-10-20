import imp
from django.shortcuts import render
from django.views.generic import DetailView
from django.db.models import Q
from lms.achievements.models import LessonAchievement
from lms.lessons.models import Lesson, LessonEnroll
from lms.steps.models import Step
from django.http import HttpResponseRedirect
from lms.topics.models import TopicEnroll


class LessonDetail(DetailView):
    model = Lesson
    template_name = 'lms/lessons/lesson_detail.html'
    slug_url_kwarg = 'lesson_slug'
    context_object_name = 'lesson'

    def get_context_data(self, **kwargs):
        context = super(LessonDetail, self).get_context_data(**kwargs)
        context['page_title'] = self.object.title
        context = self.get_steps(context)
        self.user_start_lesson()
        self.user_start_topic()

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

    def user_start_lesson(self):
        LessonEnroll.objects.get_or_create(
            lesson=self.object,
            user=self.request.user
        )

    def user_start_topic(self):
        topic_enroll = TopicEnroll.objects.get_or_create(topic=self.object.topic,
                                                         user=self.request.user)

    def user_end_lesson(request, course_slug, topic_slug, lesson_slug):
        lesson_enroll = LessonEnroll.objects.get(
            lesson=Lesson.objects.get(slug=lesson_slug), user=request.user)
        if lesson_enroll.status == 'PR' or lesson_enroll.status == 'RP':
            lesson_enroll.status = 'OK'
            LessonAchievement.objects.get_or_create(user=request.user,
                                                    points=lesson_enroll.lesson.points,
                                                    for_what=lesson_enroll.lesson)
            request.user.coin += lesson_enroll.lesson.points
            request.user.save()
            lesson_enroll.save()

        return HttpResponseRedirect(request.META['HTTP_REFERER'])


class LessonStatistics(DetailView):
    model = Lesson
    template_name = 'lms/lessons/lesson_statistics.html'
    slug_url_kwarg = 'lesson_slug'
    context_object_name = 'lesson'

    def get_context_data(self, **kwargs):
        context = super(LessonStatistics, self).get_context_data(**kwargs)
        context['page_title'] = 'Статистика урока:' + self.object.title
        context = self.get_steps(context)
        context['all_users'] = [
            enroll.user for enroll in LessonEnroll.objects.filter(lesson=self.object)]
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
