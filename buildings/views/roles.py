from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.utils.translation import ugettext as _
from django.db import transaction
from django.shortcuts import redirect
from django.views.generic import CreateView

from app.mixins import CustomUserMixin
from buildings.models import Building
from buildings.models import BuildingMembership
from buildings.permissions import BuildingPermissions
from buildings.forms import MembershipForm


class MembershipListView(CustomUserMixin, ListView):
    """
    List view with the membershpis
    created for a building or condo.
    """
    model = BuildingMembership
    template_name = 'buildings/administrative/roles/memberships_list.html'
    context_object_name = 'memberships_list'

    def test_func(self):
        return BuildingPermissions.can_manage_roles(
            user=self.request.user,
            building=self.get_object(),
        )

    def get_object(self, queryset=None):
        return get_object_or_404(
            Building,
            pk=self.kwargs['pk'],
        )

    def get_queryset(self):
        return BuildingMembership.objects.filter(
            building=self.get_object(),
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['building'] = self.get_object()
        context['active_roles'] = True

        return context


class MembershipFormView(CustomUserMixin, CreateView):
    """
    Form view to register a new membership into a building.
    """
    model = BuildingMembership
    form_class = MembershipForm
    template_name = 'buildings/administrative/roles/membership_form.html'

    def test_func(self):
        return BuildingPermissions.can_manage_roles(
            user=self.request.user,
            building=self.get_object(),
        )

    def get_object(self, queryset=None):
        return get_object_or_404(
            Building,
            pk=self.kwargs['pk'],
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['unit'] = self.get_object()
        context['building'] = self.get_object()
        # Returned to activate the correct tab in the side bar.
        context['active_roles'] = True

        return context

    @transaction.atomic
    def form_valid(self, form):
        # Create membership object.
        membership = form.save(commit=False)
        membership.building = self.get_object()
        membership.save()

        messages.success(
            self.request,
            _('Membersía creada exitosamente.')
        )

        return redirect(self.get_object().get_absolute_url())
