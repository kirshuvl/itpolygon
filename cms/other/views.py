from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView, TemplateView, FormView
from lms.courses.models import Course
from lms.topics.models import Topic
from lms.lessons.models import Lesson
from lms.steps.models import Step, StepEnroll, TextStep, VideoStep, QuestionStep, LessonStepConnection
from lms.problems.models import ProblemStep, TestForProblemStep, TestUserAnswer, UserAnswerForProblemStep
from lms.assignment.models import AssignmentStep, UserAnswerForAssignmentStep
from users.models import CustomUser
from lms.problems.tasks import run_user_code
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


from cms.constructor.text_step.forms import TextStepCreateForm


class PermissonMixin(PermissionRequiredMixin):
    def get_permission_required(self):

        return self.request.user.is_superuser,


class CMS_Dashboard(LoginRequiredMixin, PermissonMixin, TemplateView):
    '''Главная страница CMS'''
    template_name = 'cms/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(CMS_Dashboard, self).get_context_data(**kwargs)
        context['page_title'] = 'CMS Dashboard'

        return context


class CMS_CourseStatistics(LoginRequiredMixin, PermissonMixin, DetailView):
    model = Course
    template_name = 'cms/courses/statistics.html'
    context_object_name = 'course'
    slug_url_kwarg = 'course_slug'

    def get_context_data(self, **kwargs):
        context = super(CMS_CourseStatistics, self).get_context_data(**kwargs)
        context['users'] = CustomUser.objects.filter(
            courses_enrolls__course=self.object).order_by('first_name')
        context['page_title'] = 'Статистика курса: ' + self.object.title

        return context

    def get_object(self):
        users = CustomUser.objects.filter(
            courses_enrolls__course__slug=self.kwargs['course_slug'])

        return get_object_or_404(Course.objects.prefetch_related(
            Prefetch('topics', queryset=Topic.objects.filter(
                is_published=True).order_by('number')),
            Prefetch('topics__lessons', queryset=Lesson.objects.filter(
                is_published=True).order_by('number')),
            Prefetch('topics__lessons__connections', queryset=LessonStepConnection.objects.filter(is_published=True).prefetch_related(
                Prefetch('step', queryset=Step.objects.prefetch_related(
                    Prefetch('connections', queryset=LessonStepConnection.objects.filter(
                        lesson__topic__course__slug=self.kwargs['course_slug']))
                )),
                Prefetch('step__steps_enrolls',
                         queryset=StepEnroll.objects.filter(user__in=users).select_related('user',))
            ).select_related('lesson').order_by('number'))
        ),
            slug=self.kwargs['course_slug'])


class CMS_CourseSubmissions(LoginRequiredMixin, PermissonMixin, ListView):
    model = UserAnswerForProblemStep
    template_name = 'cms/courses/problems.html'
    context_object_name = 'all_attempts'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = Course.objects.get(slug=self.kwargs['course_slug'])
        context['page_title'] = 'Все посылки курса'
        return context

    def get_queryset(self):
        return UserAnswerForProblemStep.objects.select_related('problem', 'user').\
            prefetch_related().\
            filter(
                problem__connections__lesson__topic__course__slug=self.kwargs['course_slug']).order_by('pk')


def rerun_submission(request, user_answer_pk):
    user_answer = UserAnswerForProblemStep.objects.get(pk=user_answer_pk)
    user_answer.verdict = 'PR'
    user_answer.cputime = 0
    user_answer.first_fail_test = 0
    user_answer.points = 0
    user_answer.save()
    TestUserAnswer.objects.filter(
        user=user_answer.user, code=user_answer).delete()
    run_user_code.delay(user_answer_pk)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


class CMS_UserAssignmentsList(LoginRequiredMixin, PermissonMixin, ListView):
    model = UserAnswerForAssignmentStep
    template_name = 'cms/steps/assignment_step/list.html'
    context_object_name = 'assignments'

    def get_queryset(self):
        return UserAnswerForAssignmentStep.objects.select_related('assignment__lesson__topic__course', 'user').filter(assignment__lesson__topic__course__authors=self.request.user)
