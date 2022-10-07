from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import View, CreateView, DetailView, UpdateView, TemplateView
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileUpdateForm
from crm.lead.forms import UserFeedBackForm
from users.models import CustomUser
from lms.courses.models import Course
from crm.lead.models import Status, UserFeedBack


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
            return redirect('UserProfile')
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
            return redirect('UserProfile')
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
        context['page_title'] = 'Мой профиль'
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
        context['page_title'] = 'Редактировать профиль'
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
