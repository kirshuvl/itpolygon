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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False

    def is_valid(self):
        errors = self.errors.as_data()
        for field in self.fields:
            if field not in errors:
                self.fields[field].widget.attrs.update(
                    {'class': 'form-control is-valid'})
            else:
                self.fields[field].widget.attrs.update(
                    {'class': 'form-control is-invalid'})
        return super().is_valid()

    def clean_user_answer(self):
        user_answer = self.cleaned_data.get('user_answer')

        if user_answer == '':
            return self.add_error('user_answer', 'Ответ не может быть пустым')

        return user_answer


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
