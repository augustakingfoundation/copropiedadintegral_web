from django.views.generic import TemplateView

from accounts.forms import SignUpForm


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['signup_form'] = SignUpForm

        return context
