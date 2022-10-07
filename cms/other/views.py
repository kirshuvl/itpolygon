from django.views.generic import TemplateView


class CMSDashboard(TemplateView):
    template_name = 'cms/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(CMSDashboard, self).get_context_data( **kwargs)
        context['page_title'] = 'CMS Dashboard'

        return context
