from crm.lead.models import UserLead, Promocode, UserFeedBack, LeadComment, Status
from django import forms


class LeadFormValidation(forms.ModelForm):
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

    def clean_parent_first_name(self):
        parent_first_name = self.cleaned_data.get(
            'parent_first_name').capitalize()
        if parent_first_name == '':
            return self.add_error('parent_first_name', 'Введите имя родителя')

        return parent_first_name

    def clean_parent_middle_name(self):
        parent_middle_name = self.cleaned_data.get(
            'parent_middle_name').capitalize()

        return parent_middle_name

    def clean_parent_last_name(self):
        parent_last_name = self.cleaned_data.get(
            'parent_last_name').capitalize()
        if parent_last_name == '':
            return self.add_error('parent_last_name', 'Введите фамилию родителя')

        return parent_last_name

    def clean_child_first_name(self):
        child_first_name = self.cleaned_data.get(
            'child_first_name').capitalize()
        if child_first_name == '':
            return self.add_error('child_first_name', 'Введите имя ребенка')

        return child_first_name

    def clean_child_middle_name(self):
        child_middle_name = self.cleaned_data.get(
            'child_middle_name').capitalize()

        return child_middle_name

    def clean_child_last_name(self):
        child_last_name = self.cleaned_data.get('child_last_name').capitalize()
        if child_last_name == '':
            return self.add_error('child_last_name', 'Введите фамилию ребенка')

        return child_last_name

    def clean_child_class(self):
        child_class = self.cleaned_data.get('child_class')
        if child_class == 'Default':
            return self.add_error('child_class', 'Выберите класс ребенка')

        return child_class

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone == '':
            return self.add_error('phone', 'Введите номер телефона')
        elif not phone.isdigit():
            return self.add_error('phone', 'Буквы в номере телефона явно лишние :)')
        elif len(phone) < 11:
            return self.add_error('phone', 'Слишком мало цифр в номере. Вводите номер в 11-значном формате')
        elif phone[0] != '7' and phone[0] != '8':
            return self.add_error('phone', 'Номер телефона должен начинаться с 7 или 8')

        return phone

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if email == '':
            return self.add_error('email', 'Введите электронную почту')

        return email

    def clean_promocode(self):
        promocode = self.cleaned_data.get('promocode')
        if promocode == '':
            self.instance.promocode = None

            return self.instance.promocode
        try:
            code = Promocode.objects.get(title=promocode)
            self.instance.promocode = code

            return promocode
        except Promocode.DoesNotExist:

            return self.add_error('promocode', 'Такого промокода нет :(')


class UserLeadForm(LeadFormValidation):
    promocode = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Промокод',
            },
        )
    )

    class Meta:
        model = UserLead
        fields = ['parent_first_name',
                  'parent_middle_name',
                  'parent_last_name',
                  'child_first_name',
                  'child_middle_name',
                  'child_last_name',
                  'child_class',
                  'phone',
                  'email',
                  'info',
                  ]
        widgets = {
            'parent_first_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Имя',
                },
            ),
            'parent_middle_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Отчество',
                },
            ),
            'parent_last_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Фамилия',
                },
            ),
            'child_first_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Имя',
                },
            ),
            'child_middle_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Отчество',
                },
            ),
            'child_last_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Фамилия',
                },
            ),
            'child_class': forms.Select(
                attrs={
                    'class': 'form-control',
                },
            ),
            'phone': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '89651979791',
                },
            ),
            'email': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'info@itpolygon.ru'
                },
            ),
            'info': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': '3',
                    'placeholder': 'Хотите задать вопрос или сообщить какую-то информацию? Пишите её тут!'
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(UserLeadForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False


class UserLeadFormUpdate(LeadFormValidation):
    class Meta:
        model = UserLead
        fields = ['parent_first_name',
                  'parent_middle_name',
                  'parent_last_name',
                  'child_first_name',
                  'child_middle_name',
                  'child_last_name',
                  'child_class',
                  'phone',
                  'email',
                  'info',
                  'promocode',
                  'course',
                  'status',
                  ]
        widgets = {
            'parent_first_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Имя',
                },
            ),
            'parent_middle_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Отчество',
                },
            ),
            'parent_last_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Фамилия',
                },
            ),
            'child_first_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Имя',
                },
            ),
            'child_middle_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Отчество',
                },
            ),
            'child_last_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Фамилия',
                },
            ),
            'child_class': forms.Select(
                attrs={
                    'class': 'form-control',
                },
            ),
            'phone': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '89651979791',
                },
            ),
            'email': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'info@itpolygon.ru',
                },
            ),
            'info': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': '3',
                    'placeholder': 'Хотите задать вопрос или сообщить какую-то информацию? Пишите её тут!',
                },
            ),
            'promocode': forms.Select(
                attrs={
                    'class': 'form-control',
                },
            ),
            'course': forms.Select(
                attrs={
                    'class': 'form-control',
                },
            ),
            'status': forms.Select(
                attrs={
                    'class': 'form-control',
                },
            ),
        }

    def __init__(self, *args, **kwargs):
        super(UserLeadFormUpdate, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False

    def clean_promocode(self):
        promocode = self.cleaned_data.get('promocode')
        if promocode is None:
            self.fields['promocode'].widget.attrs.update(
                {'class': 'form-control is-valid'})

            return None
        return promocode

    def clean_course(self):
        course = self.cleaned_data.get('course')
        if course is None:
            return self.add_error('course', 'Выберите курс')

        return course

    def clean_status(self):
        status = self.cleaned_data.get('status')
        if status is None:
            return self.add_error('status', 'Выберите статус')

        return status


class UserFeedBackForm(LeadFormValidation):
    class Meta:
        model = UserFeedBack
        fields = ['parent_first_name',
                  'parent_middle_name',
                  'parent_last_name',
                  'phone', 'email'
                  ]
        widgets = {
            'parent_first_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Имя',
                },
            ),
            'parent_middle_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Отчество',
                },
            ),
            'parent_last_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Фамилия',
                },
            ),
            'phone': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '89651979791',
                },
            ),
            'email': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'info@itpolygon.ru',
                },
            ),
        }

    def __init__(self, *args, **kwargs):
        super(UserFeedBackForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False


class LeadCommentForm(forms.ModelForm):
    class Meta:
        model = LeadComment
        fields = ['text',
                  'status'
                  ]
        widgets = {
            'text': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': '5',
                    'placeholder': 'Текст комментария',
                },
            ),
            'status': forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Статус комментария',
                },
            ),
        }

    def __init__(self, *args, **kwargs):
        super(LeadCommentForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False

    def is_valid(self):
        errors = self.errors.as_data()
        for field in self.fields:
            if field not in errors:
                self.fields[field].widget.attrs.update(
                    {
                        'class': 'form-control is-valid'
                    }
                )
            else:
                self.fields[field].widget.attrs.update(
                    {
                        'class': 'form-control is-invalid'
                    }
                )
        return super().is_valid()

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if text == '':
            return self.add_error('text', 'Введите комментарий')
        return text

    def clean_status(self):
        status = self.cleaned_data.get('status')
        if status is None:
            return self.add_error('status', 'Выберите статус комментария')
        return status
