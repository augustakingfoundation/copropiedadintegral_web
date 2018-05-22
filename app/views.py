from django.views.generic import TemplateView

from django.shortcuts import redirect


class HomeView(TemplateView):
    template_name = 'home.html'


# TODO: ADD permission
class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    def get(self, request, *args, **kwargs):
        user = request.user

        if not user.is_verified:
            return redirect('accounts:unverified_email')

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context
