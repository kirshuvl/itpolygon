from django.views.generic import ListView
from lms.achievements.models import StepAchievement
from django.contrib.auth.mixins import LoginRequiredMixin


class UserAchievements(LoginRequiredMixin, ListView):
    model = StepAchievement
    template_name = 'lms/achievements/list.html'
    context_object_name = 'achievements'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserAchievements, self).get_context_data(**kwargs)

        return context

    def get_queryset(self):
        return StepAchievement.objects.select_related('for_what').filter(user=self.request.user).order_by('-date_create')
