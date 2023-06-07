from lms.steps.forms import UserAnswerForQuestionChoiceStepForm, UserAnswerForQuestionStepForm
from lms.steps.mixins import BaseStepMixin
from lms.steps.models import QuestionChoiceStep, UserAnswerForQuestionChoiceStep, UserAnswerForQuestionStep, QuestionStep, StepEnroll

from django.views.generic import CreateView


class LMS_TextStepDetail(BaseStepMixin):
    template_name = 'lms/steps/text_step/detail.html'


class LMS_VideoStepDetail(BaseStepMixin):
    template_name = 'lms/steps/video_step/detail.html'


class LMS_QuestionStepDetail(BaseStepMixin, CreateView):
    template_name = 'lms/steps/question_step/detail.html'
    form_class = UserAnswerForQuestionStepForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_attempts'] = self.get_user_attempts()
        context['all_attempts'] = self.get_all_attempts()
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.user_answer = form.cleaned_data['user_answer']
        form.instance.question = QuestionStep.objects.get(
            slug=self.kwargs['step_slug'])
        step_enroll = StepEnroll.objects.get(
            user=self.request.user, step=form.instance.question)
        if form.cleaned_data['user_answer'] == form.instance.question.answer:
            form.instance.is_correct = True
            step_enroll.status = 'OK'
        else:
            form.instance.is_correct = False
            step_enroll.status = 'WA'
        step_enroll.save()

        return super().form_valid(form)

    def get_success_url(self):
        return self.object.question.get_lms_detail_url()

    def get_all_attempts(self):
        if self.request.user == self.object.author:
            return UserAnswerForQuestionStep.objects.filter(question=self.object).select_related('user', 'question')

        return None

    def get_user_attempts(self):

        return UserAnswerForQuestionStep.objects.filter(user=self.request.user, question=self.object).select_related('user', 'question')


class LMS_QuestionChoiceStepDetail(BaseStepMixin, CreateView):
    template_name = 'lms/steps/question_choice_step/detail.html'
    form_class = UserAnswerForQuestionChoiceStepForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_attempts'] = self.get_user_attempts()
        context['all_attempts'] = self.get_all_attempts()
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.question = QuestionChoiceStep.objects.get(
            slug=self.kwargs['step_slug'])
        step_enroll = StepEnroll.objects.get(
            user=self.request.user, step=form.instance.question)
        if form.instance.user_answer.is_correct:
            form.instance.is_correct = True
            step_enroll.status = 'OK'
        elif not form.instance.user_answer.is_correct and step_enroll.status != 'OK':
            form.instance.is_correct = False
            step_enroll.status = 'WA'
        step_enroll.save()

        return super(LMS_QuestionChoiceStepDetail, self).form_valid(form)

    def get_all_attempts(self):
        if self.request.user == self.object.author:
            return UserAnswerForQuestionChoiceStep.objects.filter(question=self.object).select_related('user', 'question').prefetch_related(
                'user_answer'
            )

        return None

    def get_user_attempts(self):

        return UserAnswerForQuestionChoiceStep.objects.filter(user=self.request.user, question=self.object).select_related('user', 'question').prefetch_related(
            'user_answer'
        )

    def get_success_url(self):
        return self.object.question.get_lms_detail_url()
