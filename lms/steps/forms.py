from django import forms
from lms.steps.models import TestForQuestionChoiceStep, UserAnswerForQuestionChoiceStep, UserAnswerForQuestionStep


class UserAnswerForQuestionStepForm(forms.ModelForm):
    class Meta:
        model = UserAnswerForQuestionStep
        fields = ['user_answer']
        widgets = {
            'user_answer': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Введите свой ответ'
                }
            )
        }


class UserAnswerForQuestionChoiceStepForm(forms.ModelForm):
    '''user_answer = forms.ModelChoiceField(queryset=TestForQuestionChoiceStep.objects.filter(question__slug=kwargs['step_slug']), 
                                    widget=forms.RadioSelect(attrs={
                    'class': 'btn-check',
                }))'''
    class Meta:
        model = UserAnswerForQuestionChoiceStep

        fields = ['user_answer']
        widgets = {
            'user_answer': forms.RadioSelect(
                attrs={
                    'class': 'btn-check',
                }
            )
        }

    def __init__(self, *args, **kwargs):
        super(UserAnswerForQuestionChoiceStepForm,
              self).__init__(*args, **kwargs)
        #print('kw', kwargs['instance'])
        if kwargs['instance'] is not None:
            self.fields['user_answer'].queryset = TestForQuestionChoiceStep.objects.filter(
                question__slug=kwargs['instance'].slug)
