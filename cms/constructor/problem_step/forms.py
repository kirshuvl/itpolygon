from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from lms.problems.models import ProblemStep
from zipfile import ZipFile
from cms.constructor.steps.forms import StepCreateForm


class ProblemStepCreateForm(StepCreateForm):
    class Meta(StepCreateForm.Meta):
        model = ProblemStep
        fields = StepCreateForm.Meta.fields + ['description',
                                               'input_format',
                                               'output_format',
                                               'notes',
                                               'start_code',
                                               'first_sample',
                                               'last_sample',
                                               'first_test',
                                               'cputime',
                                               'memory',
                                               'num_attempts'
                                               ]
        widgets = StepCreateForm.Meta.widgets | {
            'input_format': CKEditorUploadingWidget(
            ),
            'output_format': CKEditorUploadingWidget(
            ),
            'notes': CKEditorUploadingWidget(
            ),
            'start_code': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': '5',
                    'placeholder': 'Код для выполнения. Место для пользовательского кода обозначьте как {{ user_code }}',
                }
            ),
            'first_sample': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Первый сэмпл',
                }
            ),
            'last_sample': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Последний сэмпл',
                }
            ),
            'first_test': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Первый тест',
                }
            ),
            'cputime': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Время',
                }
            ),
            'memory': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Память',
                }
            ),
            'num_attempts': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Количество попыток',
                }
            ),
        }


class TestForProblemStepForm(forms.Form):
    zip_file = forms.FileField(
        widget=forms.FileInput(
            attrs={
                'class': 'form-control', 'placeholder': 'Выбрать файл'
            }
        )
    )
    rewrite = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input',
                'placeholder': 'Опубликовать',
                'role': 'switch'
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super(TestForProblemStepForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False

    def clean_zip_file(self):
        zip_file = self.cleaned_data.get('zip_file')

        if zip_file is None:
            return self.add_error('zip_file', 'Выберите файл')

        with ZipFile(zip_file, 'r') as file:
            data = self.open_file(file)

        return data

    def open_file(self, file):
        data = {}

        for cur_file in file.infolist():
            with file.open(cur_file) as cur_f:
                data[cur_file.filename] = str(
                    cur_f.read(), encoding='UTF-8').replace('\r', '')

        if len(data) % 2 == 1:
            return self.add_error('zip_file', 'Количество файлов нечетное, значит не хватает какого-то теста')

        loc_data = sorted(data)
        for el in range(0, len(data), 2):
            if not (loc_data[el][:2] == loc_data[el + 1][:2] and loc_data[el][2:] == '_in.txt' and
                    loc_data[el + 1][2:] == '_out.txt' and int(loc_data[el][:2]) == el // 2 + 1 and
                    int(loc_data[el + 1][:2]) == el // 2 + 1):
                return self.add_error('zip_file', 'Что-то пошло не так. Перепроверьте тесты. Возможно пропущен тест')
        file_data = {}

        for el in range(1, len(sorted(data)) // 2 + 1, 1):
            file_data[el] = {'input': data['{}_in.txt'.format(str(el).zfill(2))],
                             'output': data['{}_out.txt'.format(str(el).zfill(2))]}

        return file_data

    def is_valid(self):
        errors = self.errors.as_data()
        for field in self.fields:
            if field == 'rewrite':
                continue
            if field not in errors:
                self.fields[field].widget.attrs.update(
                    {'class': 'form-control is-valid'})
            else:
                self.fields[field].widget.attrs.update(
                    {'class': 'form-control is-invalid'})
        return super().is_valid()
