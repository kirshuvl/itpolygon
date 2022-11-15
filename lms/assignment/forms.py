from django import forms
from lms.assignment.models import UserAnswerForAssignmentStep


class UserAnswerForAssignmentStepForm(forms.ModelForm):
    class Meta:
        model = UserAnswerForAssignmentStep
        fields = ['user_answer', 'file']
        widgets = {
            'user_answer': forms.Textarea(
                attrs={
                        'class': 'form-control',
                        'rows': '5',
                        'placeholder': 'Тут какой-то текст, если требуется'
                    }
            ),
            'file': forms.FileInput(
                    attrs={
                        'class': 'form-control',
                        'placeholder': 'Файл'
                    }
            ),
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
            return self.add_error('user_answer', 'Напишите что-нибудь о своей работе')

        return user_answer

    def clean_file(self):
        file = self.cleaned_data.get('file')

        if file is None:
            return self.add_error('file', 'Выберите файл')

        return file
