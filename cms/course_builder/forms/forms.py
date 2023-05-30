from django import forms
from lms.courses.models import Course
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from lms.problems.models import ProblemStep
from lms.steps.models import QuestionStep, Step, TextStep, VideoStep
from zipfile import ZipFile

from lms.assignment.models import AssignmentStep


class MixinForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False

    def is_valid(self):
        errors = self.errors.as_data()
        for field in self.fields:
            if field == 'is_published':
                continue
            if field not in errors:
                self.fields[field].widget.attrs.update(
                    {'class': 'form-control is-valid'})
            else:
                self.fields[field].widget.attrs.update(
                    {'class': 'form-control is-invalid'})
        return super().is_valid()

    def clean_title(self):
        title = self.cleaned_data.get('title')

        if title == '':
            return self.add_error('title', 'Название не может быть пустым')

        return title

    def clean_slug(self):
        slug = self.cleaned_data.get('slug').lower()

        if slug == '':
            return self.add_error('slug', 'URL не может быть пустым')

        return slug

    def clean_icon(self):
        icon = self.cleaned_data.get('icon')

        if icon is None:
            return self.add_error('icon', 'Выберите картинку')

        return icon

    def clean_description(self):
        description = self.cleaned_data.get('description')

        if description == '':
            return self.add_error('description', 'Введите краткое описание')

        return description

    def clean_input_format(self):
        input_format = self.cleaned_data.get('input_format')

        if input_format == '':
            return self.add_error('input_format', 'Не указан формат ввода')

        return input_format

    def clean_output_format(self):
        output_format = self.cleaned_data.get('output_format')

        if output_format == '':
            return self.add_error('output_format', 'Не указан формат вывода')

        return output_format

    def clean_full_description(self):
        full_description = self.cleaned_data.get('full_description')

        if full_description == '':
            return self.add_error('full_description', 'Введите полное описание')

        return full_description

    def clean_category(self):
        category = self.cleaned_data.get('category')

        if category is None:
            return self.add_error('category', 'Выберите категорию')

        return category

    def clean_tags(self):
        tags = self.cleaned_data.get('tags')

        if not tags:
            return self.add_error('tags', 'Выберите соответствующие теги')

        return tags

    def clean_answer(self):
        answer = self.cleaned_data.get('answer')

        if answer == '':
            return self.add_error('answer', 'Введите ответ')

        return answer

    def clean_num_attempts(self):
        num_attempts = self.cleaned_data.get('num_attempts')
        if num_attempts == 0 or num_attempts is None:
            return self.add_error('num_attempts', 'Введите количество попыток')

        return num_attempts

    def clean_points(self):
        points = self.cleaned_data.get('points')

        if points == 0 or points is None:
            return self.add_error('points', 'Не обесценивайте работу учеников')

        return points

    def clean_video_url(self):
        video_url = self.cleaned_data.get('video_url')

        if video_url == '':
            return self.add_error('video_url', 'Прикрепите ссылку на видео')

        return video_url

    def clean_cputime(self):
        cputime = self.cleaned_data.get('cputime')
        if cputime == 0 or cputime is None:
            return self.add_error('cputime', 'Введите время на тест')

        return cputime

    def clean_memory(self):
        memory = self.cleaned_data.get('memory')
        if memory == 0 or memory is None:
            return self.add_error('memory', 'Выделите память на задачу')

        return memory

    def clean_first_sample(self):
        first_sample = self.cleaned_data.get('first_sample')
        if first_sample == 0 or first_sample is None:
            return self.add_error('first_sample', 'Номер первого сэмпла')

        return first_sample

    def clean_last_sample(self):
        last_sample = self.cleaned_data.get('last_sample')
        if last_sample == 0 or last_sample is None:
            return self.add_error('last_sample', 'Номер последнего сэмпла')

        return last_sample

    def clean_first_test(self):
        first_test = self.cleaned_data.get('first_test')
        if first_test == 0 or first_test is None:
            return self.add_error('first_test', 'Номер первого теста')

        return first_test



class StepCreateForm(MixinForm):
    class Meta:
        model = Step
        fields = ['title',
                  'slug',
                  'description',
                  'is_published',
                  'points',
                  ]
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Заголовок шага',
                }
            ),
            'slug': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Slug шага',
                }
            ),
            'description': CKEditorUploadingWidget(),
            'is_published': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                    'placeholder': 'Опубликовать',
                    'role': 'switch',
                }
            ),
            'points': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Баллы за шаг',
                }
            ),
        }


class TextStepCreateForm(StepCreateForm):
    class Meta(StepCreateForm.Meta):
        model = TextStep
        fields = StepCreateForm.Meta.fields + ['text']
        widgets = StepCreateForm.Meta.widgets


class VideoStepCreateForm(StepCreateForm):
    class Meta(StepCreateForm.Meta):
        model = VideoStep
        fields = StepCreateForm.Meta.fields + ['video_url']
        widgets = StepCreateForm.Meta.widgets | {
            'video_url': forms.URLInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ссылка на видео',
                }
            ),
        }


class QuestionStepCreateForm(StepCreateForm):
    class Meta(StepCreateForm.Meta):
        model = QuestionStep
        fields = StepCreateForm.Meta.fields + ['answer', 'num_attempts']
        widgets = StepCreateForm.Meta.widgets | {
            'answer': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Правильный ответ',
                }
            ),
            'num_attempts': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Количество попыток',
                }
            ),
        }


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


class AssignmentStepCreateForm(StepCreateForm):
    class Meta(StepCreateForm.Meta):
        model = AssignmentStep
        fields = StepCreateForm.Meta.fields + ['file']
        widgets = StepCreateForm.Meta.widgets | {
            'file': forms.FileInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Файл'
                }
            ),
        }
