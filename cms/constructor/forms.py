from django import forms


class MixinForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False

    def is_valid(self):
        errors = self.errors.as_data()
        for field in self.fields:
            if field == 'is_published' or field == 'is_search':
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

    '''def clean_input_format(self):
        input_format = self.cleaned_data.get('input_format')

        if input_format == '':
            return self.add_error('input_format', 'Не указан формат ввода')

        return input_format

    def clean_output_format(self):
        output_format = self.cleaned_data.get('output_format')

        if output_format == '':
            return self.add_error('output_format', 'Не указан формат вывода')

        return output_format'''

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
