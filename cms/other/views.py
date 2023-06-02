from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView, TemplateView, FormView
from lms.courses.models import Course
from lms.topics.models import Topic
from lms.lessons.models import Lesson
from lms.steps.models import Step, StepEnroll, TextStep, VideoStep, QuestionStep
from lms.problems.models import ProblemStep, TestForProblemStep, TestUserAnswer, UserAnswerForProblemStep
from lms.assignment.models import AssignmentStep, UserAnswerForAssignmentStep
from users.models import CustomUser
from cms.course_builder.forms.forms import \
    TestForProblemStepForm, \
    VideoStepCreateForm, QuestionStepCreateForm, ProblemStepCreateForm, AssignmentStepCreateForm
from lms.problems.tasks import run_user_code
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class CMS_Dashboard(LoginRequiredMixin, TemplateView):
    '''Главная страница CMS'''
    template_name = 'cms/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(CMS_Dashboard, self).get_context_data(**kwargs)
        context['page_title'] = 'CMS Dashboard'

        return context


class CMS_CourseStatistics(DetailView):
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

        return get_object_or_404(
            Course.objects.prefetch_related(
                Prefetch('topics', queryset=Topic.objects.filter(
                    is_published=True).order_by('number')),
                Prefetch('topics__lessons', queryset=Lesson.objects.filter(
                    is_published=True).order_by('number')),
                Prefetch('topics__lessons__steps', queryset=Step.objects.filter(
                    is_published=True).order_by('number')),
                Prefetch('topics__lessons__steps__steps_enrolls',
                         queryset=StepEnroll.objects.select_related('user')),
            ),
            slug=self.kwargs['course_slug']
        )


class CMS_CourseSubmissions(ListView):
    model = UserAnswerForProblemStep
    template_name = 'cms/courses/problems.html'
    context_object_name = 'users_attempts'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super(CMS_CourseSubmissions, self).get_context_data(**kwargs)
        context['course'] = Course.objects.get(slug=self.kwargs['course_slug'])

        return context

    def get_queryset(self):
        return UserAnswerForProblemStep.objects.select_related('problem__lesson__topic__course', 'user').filter(problem__lesson__topic__course__slug=self.kwargs['course_slug'])




def step_check_publish(request, step_slug):
    step = Step.objects.get(slug=step_slug)
    if step.is_published:
        step.is_published = False
    else:
        step.is_published = True
    step.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])




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


class CMS_UserAssignmentsList(ListView):
    model = UserAnswerForAssignmentStep
    template_name = 'cms/steps/assignment_step/list.html'
    context_object_name = 'assignments'

    def get_queryset(self):
        return UserAnswerForAssignmentStep.objects.select_related('assignment__lesson__topic__course', 'user').filter(assignment__lesson__topic__course__authors=self.request.user)
