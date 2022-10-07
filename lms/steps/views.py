from audioop import reverse
from lms.achievements.models import StepAchievement
from lms.steps.forms import UserAnswerForQuestionStepForm
from lms.steps.mixins import BaseStepMixin
from lms.steps.models import TextStep, UserAnswerForQuestionStep, VideoStep, QuestionStep, StepEnroll
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView


class TextStepDetail(BaseStepMixin):
    model = TextStep
    template_name = 'lms/steps/text_step_detail.html'

    def get_object(self):
        return get_object_or_404(TextStep.objects.select_related('lesson__topic__course'),
                                 slug=self.kwargs['step_slug'])


class VideoStepDetail(BaseStepMixin):
    model = VideoStep
    template_name = 'lms/steps/video_step_detail.html'

    def get_object(self):
        return get_object_or_404(VideoStep.objects.select_related('lesson__topic__course'),
                                 slug=self.kwargs['step_slug'])


class QuestionStepDetail(BaseStepMixin, CreateView):
    model = QuestionStep
    template_name = 'lms/steps/question_step_detail.html'
    form_class = UserAnswerForQuestionStepForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['attempts'] = UserAnswerForQuestionStep.objects.filter(
            user=self.request.user, question=self.object)
        return context

    def get_object(self):
        return get_object_or_404(QuestionStep.objects.select_related('lesson__topic__course', ).prefetch_related('question_answers'),
                                 slug=self.kwargs['step_slug'])

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.user_answer = form.cleaned_data['user_answer']
        form.instance.question = QuestionStep.objects.get(
            slug=self.kwargs['step_slug'])
        step_enroll = StepEnroll.objects.filter(
            user=self.request.user, step=form.instance.question).first()
        if form.cleaned_data['user_answer'] == form.instance.question.answer:
            form.instance.is_correct = True
            step_enroll.status = 'OK'
            StepAchievement.objects.get_or_create(user=self.request.user,
            points=step_enroll.step.points,
            for_what=step_enroll.step,
            )
            self.request.user.coin += step_enroll.step.points
            self.request.user.save()
        else:
            form.instance.is_correct = False
            step_enroll.status = 'WA'
        step_enroll.save()

        return super(QuestionStepDetail, self).form_valid(form)
