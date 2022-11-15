from django import forms
from lms.steps.models import UserAnswerForQuestionStep


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
