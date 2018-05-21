from django.views.generic import TemplateView

from accounts.forms import SignUpForm
from accounts.forms import LoginForm


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['signup_form'] = SignUpForm
        context['login_form'] = LoginForm(prefix='login')

        return context


class DashboardView(TemplateView):
    template_name = 'dashboard.html'
