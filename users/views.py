from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import View, CreateView, DetailView, UpdateView, TemplateView, ListView
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileUpdateForm
from crm.lead.forms import UserFeedBackForm
from users.models import CustomUser
from lms.courses.models import Course
from crm.lead.models import Status, UserFeedBack
import datetime as dt
from lms.steps.models import *
from lms.problems.models import *
from django.db.models import Prefetch
from django.db.models import Q
from polymorphic.managers import PolymorphicQuerySet
from lms.assignment.models import AssignmentStep
from polymorphic.utils import *
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from django.db.models.functions import TruncDate
from itertools import groupby
from collections import defaultdict

class HomePage(CreateView):
    model = UserFeedBack
    form_class = UserFeedBackForm
    template_name = 'main/home_page.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(HomePage, self).get_context_data(**kwargs)
        context['page_title'] = 'IT Polygon - онлайн образование для будущих инженеров и программистов'
        context['courses'] = Course.objects.filter(is_published=True)
        return context

    def form_valid(self, form):
        try:
            form.instance.status = Status.objects.get(title='Новая заявка')
        except Status.DoesNotExist:
            form.instance.status = None
        messages.add_message(self.request, messages.SUCCESS,
                             'Отлично! Ваша заявка принята. Мы свяжемся с Вами в ближайшее время')
        return super(HomePage, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('HomePage')


class UserLogin(TemplateView):
    form_class = UserLoginForm
    template_name = 'users/login.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            username = form.clean_username()
            password = form.clean_password()
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
            return redirect('LMS_UserProfile')
        return render(request, self.template_name, context={'form': form})


class UserRegistration(CreateView):
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'

    def post(self, request, *args, **kwargs):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return redirect('LMS_UserProfile')
        else:
            messages.error(request, 'Ошибка регистрации')
            return render(request, self.template_name, {'form': form})


class UserResetPassword(TemplateView):
    template_name = 'users/reset.html'

    def get_context_data(self, **kwargs):
        context = super(UserResetPassword, self).get_context_data(**kwargs)
        context['page_title'] = 'Восстановить пароль'

        return context


class UserLogout(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('HomePage')


class UserProfile(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'users/profile.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super(UserProfile, self).get_context_data()
        return context

    def get_object(self):
        return get_object_or_404(CustomUser, id=self.request.user.id)


class UserProfileUpdate(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = UserProfileUpdateForm
    template_name = 'users/profile_update.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super(UserProfileUpdate, self).get_context_data(**kwargs)
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(CustomUser, id=self.request.user.id)

    def get_success_url(self):
        return reverse_lazy('UserProfile')


class ShuvalovView(TemplateView):
    template_name = 'main/shuvalov.html'

    def get_context_data(self, **kwargs):
        context = super(ShuvalovView, self).get_context_data(**kwargs)
        context['page_title'] = 'Шувалов Кирилл Сергеевич'

        return context


class UserStatistics(TemplateView):

    template_name = 'users/statistics.html'

    def get_context_data(self, **kwargs,):
        context = super(UserStatistics, self).get_context_data(**kwargs)
        context['enrolls'] = self.get_data()
        context['current_user'] = CustomUser.objects.get(
            nickname=self.kwargs['nickname'])
        #context['enrolls'] = self.get_statistics()

        return context

    def get_start_day(self, months, weeks):

        current_date = dt.datetime.today().date()
        num_months = months
        num_weeks = weeks
        w = (num_months * num_weeks - 1) * 7 + \
            current_date.isocalendar().weekday - 1
        start_day = current_date + dt.timedelta(days=-w)

        return start_day

    def get_data_dict(self):
        current_date = dt.datetime.today().date()
        num_months = 9
        num_weeks = 4
        all_days = (num_months * num_weeks - 1) * 7 + \
            current_date.isocalendar().weekday - 1
        start_day = current_date + dt.timedelta(days=-all_days)
        data = defaultdict(lambda: lambda: defaultdict(list))
        for i in range(all_days + 1):
            data[start_day] = defaultdict(lambda: defaultdict(list))
            start_day += dt.timedelta(days=1)

        queryset = StepEnroll.objects.filter(user__nickname=self.kwargs['nickname']).\
            select_related('step__lesson__topic__course').\
            prefetch_related('step',
                             'step__textstep',
                             'step__videostep',
                             'step__questionstep',
                             'step__questionchoicestep',
                             'step__problemstep', 'step__assignmentstep').order_by('date_create')

        for enroll in queryset:
            if enroll.step.child_type == 'textstep':
                if enroll.status == 'OK':
                    if enroll.date_create.date() == enroll.date_update.date():
                        data[enroll.date_create.date()][enroll.step.child_type]['all'].append(enroll)
                    else:
                        data[enroll.date_create.date()][enroll.step.child_type]['start'].append(enroll)
                        data[enroll.date_update.date()][enroll.step.child_type]['end'].append(enroll)
                else:
                    if enroll.date_create.date() == enroll.date_update.date():
                        data[enroll.date_create.date()][enroll.step.child_type]['start'].append(enroll)
                    else:
                        data[enroll.date_create.date()][enroll.step.child_type]['start'].append(enroll)
                        data[enroll.date_update.date()][enroll.step.child_type]['end'].append(enroll)


        
        #print(data)
        

        return data

    def get_data(self):

        data_dict = self.get_data_dict()

        current_date = dt.datetime.today().date()
        data = {}
        num_months = 9
        num_weeks = 4
        w = (num_months * num_weeks - 1) * 7 + \
            current_date.isocalendar().weekday - 1
        start_day = current_date + dt.timedelta(days=-w)

        for month in range(num_months):
            data['month_{}'.format(month)] = {}
            for week in range(num_weeks):
                data['month_{}'.format(month)]['week_{}'.format(week)] = {}
                for day in range(7):
                    if start_day <= current_date:
                        data['month_{}'.format(month)]['week_{}'.format(week)][start_day] = data_dict[start_day]
                    start_day += dt.timedelta(days=1)
        return data
