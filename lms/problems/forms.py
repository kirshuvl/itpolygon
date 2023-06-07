import imp
from django import forms
from lms.problems.models import UserAnswerForProblemStep


class ProblemUpload(forms.ModelForm):
    code = forms.FileField(
        widget=forms.FileInput(
            attrs={
                'class': 'form-control', 'placeholder': 'Выбрать файл'
            }
        )
    )

    class Meta:
        model = UserAnswerForProblemStep
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(ProblemUpload, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False
        #self.fields['code'].required = True

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

    def clean_code(self):
        file = self.cleaned_data.get('code')
        if file is None:
            return self.add_error('code', 'Нет кода - нет проверки. Вы забыли прикрепить свой файл')

        file = file.open().read()

        return str(file, encoding='UTF-8')
