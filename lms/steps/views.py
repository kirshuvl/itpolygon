from lms.steps.forms import UserAnswerForQuestionChoiceStepForm, UserAnswerForQuestionStepForm
from lms.steps.mixins import BaseStepMixin
from lms.steps.models import QuestionChoiceStep, UserAnswerForQuestionChoiceStep, UserAnswerForQuestionStep, QuestionStep, StepEnroll

from django.views.generic import CreateView


class TextStepDetail(BaseStepMixin):
    template_name = 'lms/steps/text_step_detail.html'


class VideoStepDetail(BaseStepMixin):
    template_name = 'lms/steps/video_step_detail.html'


class QuestionStepDetail(BaseStepMixin, CreateView):
    template_name = 'lms/steps/question_step_detail.html'
    form_class = UserAnswerForQuestionStepForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['attempts'] = UserAnswerForQuestionStep.objects.filter(
            user=self.request.user, question=self.object)
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

        return super(QuestionStepDetail, self).form_valid(form)


class QuestionChoiceStepDetail(BaseStepMixin, CreateView):
    template_name = 'lms/steps/question_choice_step_detail.html'
    form_class = UserAnswerForQuestionChoiceStepForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['attempts'] = UserAnswerForQuestionChoiceStep.objects.filter(
            user=self.request.user, question=self.object)
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.question = QuestionChoiceStep.objects.get(
            slug=self.kwargs['step_slug'])
        step_enroll = StepEnroll.objects.get(
            user=self.request.user, step=form.instance.question)
        if form.instance.user_answer.is_correct and step_enroll.status != 'OK':
            form.instance.is_correct = True
            step_enroll.status = 'OK'
        elif not form.instance.user_answer.is_correct and step_enroll.status != 'OK':
            form.instance.is_correct = False
            step_enroll.status = 'WA'
        step_enroll.save()


        return super(QuestionChoiceStepDetail, self).form_valid(form)
