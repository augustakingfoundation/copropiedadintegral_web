from django.shortcuts import redirect
from django.views.generic import TemplateView

from accounts.permissions import UserPermissions
from app.mixins import CustomUserMixin
from buildings.models import BuildingMembership


class HomeView(TemplateView):
    template_name = 'home.html'


class DashboardView(CustomUserMixin, TemplateView):
    template_name = 'dashboard.html'

    def test_func(self):
        return UserPermissions.can_view_dashboard(
            user=self.request.user,
        )

    def get(self, request, *args, **kwargs):
        user = request.user

        if not user.is_verified:
            return redirect('accounts:unverified_email')

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['memberships'] = BuildingMembership.objects.filter(
            user=self.request.user,
            is_active=True,
        )

        return context
