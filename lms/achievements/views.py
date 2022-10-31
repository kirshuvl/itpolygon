from django.views.generic import ListView
from lms.achievements.models import Achievement, StepAchievement

# Create your views here.


class UserAchievements(ListView):
    model = StepAchievement
    template_name = 'lms/achievements/user_achievement_list.html'
    context_object_name = 'achievements'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserAchievements, self).get_context_data(**kwargs)
        context['page_title'] = 'Мои достижения'
        return context

    def get_queryset(self):
        return Achievement.objects.filter(user=self.request.user).order_by('-date_create')
