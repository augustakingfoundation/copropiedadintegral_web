from django.conf import settings
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.utils.translation import ugettext as _
from django.template.loader import render_to_string
from django.db import transaction
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic import FormView
from django.urls import reverse

from app.mixins import CustomUserMixin
from buildings.models import Building
from buildings.models import BuildingMembership
from buildings.permissions import RolesPermissions
from buildings.forms import MembershipForm
from buildings.forms import UserSearchForm
from buildings.forms import membershipTransferForm
from buildings.data import MEMBERSHIP_TYPE_ADMINISTRATOR
from app.tasks import send_email


class MembershipListView(CustomUserMixin, ListView):
    """
    List view with the membershpis
    created for a building or condo.
    """
    model = BuildingMembership
    template_name = 'buildings/administrative/roles/memberships_list.html'
    context_object_name = 'memberships_list'

    def test_func(self):
        return RolesPermissions.can_manage_roles(
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
        return RolesPermissions.can_manage_roles(
            user=self.request.user,
            building=self.get_object(),
        )

    def get_object(self, queryset=None):
        return get_object_or_404(
            Building,
            pk=self.kwargs['pk'],
        )

    def get_form_kwargs(self):
        building = self.get_object()

        # Get authenticated user membership
        membership = BuildingMembership.objects.get(
            user=self.request.user,
            building=building,
        )

        kwargs = super().get_form_kwargs()
        kwargs['building'] = building
        kwargs['membership'] = membership
        kwargs['update'] = False

        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['unit'] = self.get_object()
        context['building'] = self.get_object()
        # Returned to activate the correct tab in the side bar.
        context['active_roles'] = True
        context['user_search_form'] = UserSearchForm()

        return context

    @transaction.atomic
    def form_valid(self, form):
        # Create membership object.
        membership = form.save(commit=False)
        membership.building = self.get_object()
        membership.is_active = True
        membership.save()

        messages.success(
            self.request,
            _('Membersía creada exitosamente.')
        )

        # Send notification email about new membership
        # to the user.
        subject = _('Se ha creado una nueva membresía en una copropiedad '
                    ' para usted.')

        body = render_to_string(
            'buildings/administrative/roles/membership_email.html', {
                'title': subject,
                'from': self.request.user,
                'membership': membership,
                'base_url': settings.BASE_URL,
            },
        )

        send_email(
            subject=subject,
            body=body,
            mail_to=[membership.user.email],
        )

        return redirect(
            'buildings:memberships_list',
            self.get_object().id,
        )


class MembershipUpdateView(CustomUserMixin, UpdateView):
    """
    Membership update view. Only administrators can manage
    memberships and the RolesPermissions.can_edit_membership
    function defines the main rules to access this view.
    """
    model = BuildingMembership
    form_class = MembershipForm
    template_name = 'buildings/administrative/roles/membership_form.html'

    def test_func(self):
        return RolesPermissions.can_edit_membership(
            user=self.request.user,
            membership=self.get_object(),
        )

    def get_object(self, queryset=None):
        return get_object_or_404(
            BuildingMembership,
            building_id=self.kwargs['b_pk'],
            pk=self.kwargs['m_pk'],
        )

    def get_form_kwargs(self):
        building = self.get_object().building
        # Get authenticated user membership
        membership = BuildingMembership.objects.get(
            user=self.request.user,
            building=building,
        )

        kwargs = super().get_form_kwargs()
        kwargs['building'] = self.get_object().building
        kwargs['membership'] = membership
        kwargs['update'] = True

        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['building'] = self.get_object().building
        # Returned to activate the correct tab in the side bar.
        context['active_roles'] = True
        context['membership_update'] = True

        return context

    def get_success_url(self):
        # Reverse to unit detail.
        return reverse(
            'buildings:memberships_list',
            args=[self.kwargs['b_pk']]
        )

    @transaction.atomic
    def form_valid(self, form):
        # Update membership object.
        membership = form.save()

        messages.success(
            self.request,
            _('Membresía actualizada exitosamente.'),
        )

        # Send email to user about his membership update.
        subject = _('Su membresía ha sido editada')

        body = render_to_string(
            'buildings/administrative/roles/membership_email.html', {
                'title': subject,
                'from': self.request.user,
                'membership': membership,
                'update': True,
                'base_url': settings.BASE_URL,
            },
        )

        send_email(
            subject=subject,
            body=body,
            mail_to=[membership.user.email],
        )

        return super().form_valid(form)


class MembershipDeleteView(CustomUserMixin, DeleteView):
    """
    Memberhips delete view. Users are redirected to a view
    in which they will be asked about confirmation for
    delete a membership definitely.
    """
    model = BuildingMembership
    template_name = 'buildings/administrative/roles/membership_delete_confirm.html'

    def test_func(self):
        return RolesPermissions.can_edit_membership(
            user=self.request.user,
            membership=self.get_object(),
        )

    def get_object(self, queryset=None):
        return get_object_or_404(
            BuildingMembership,
            building_id=self.kwargs['b_pk'],
            pk=self.kwargs['m_pk'],
        )

    def get_success_url(self):
        # Reverse to roles module detail.
        return reverse(
            'buildings:memberships_list',
            args=[self.kwargs['b_pk']]
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['building'] = self.get_object().building
        # Returned to activate the correct tab in the side bar.
        context['active_roles'] = True
        context['membership_update'] = True

        return context

    def delete(self, request, *args, **kwargs):
        messages.success(
            self.request,
            _('Membresía eliminada exitosamente.')
        )

        # Send email to user about his membership delete.
        subject = _('Su membresía ha sido eliminada')

        body = render_to_string(
            'buildings/administrative/roles/membership_email.html', {
                'title': subject,
                'from': self.request.user,
                'membership': self.get_object(),
                'delete': True,
                'base_url': settings.BASE_URL,
            },
        )

        send_email(
            subject=subject,
            body=body,
            mail_to=[self.get_object().user.email],
        )

        return super().delete(request, *args, **kwargs)


class MembershipTransferView(CustomUserMixin, FormView):
    form_class = membershipTransferForm
    template_name = 'buildings/administrative/roles/membership_transfer.html'

    def test_func(self):
        return RolesPermissions.can_transfer_membership(
            user=self.request.user,
            membership=self.get_object(),
        )

    def get_object(self, queryset=None):
        return get_object_or_404(
            BuildingMembership,
            building_id=self.kwargs['b_pk'],
            pk=self.kwargs['m_pk'],
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['building'] = self.get_object().building
        # Returned to activate the correct tab in the side bar.
        context['active_roles'] = True
        # Membership can be transfered only to active administrator
        # users. If there are not active adimistrators, the membership
        # can't be transfered.
        context['display_transfer_form'] = self.get_administrators_queryset()

        return context

    def get_administrators_queryset(self):
        membership = self.get_object()
        building = membership.building

        return BuildingMembership.objects.filter(
            building=building,
            membership_type=MEMBERSHIP_TYPE_ADMINISTRATOR,
            user__is_active=True,
            user__is_verified=True,
            is_active=True,
        ).exclude(user__id=membership.user.id)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['administrators_queryset'] = self.get_administrators_queryset()
        return kwargs

    @transaction.atomic
    def form_valid(self, form):
        # Get user to transfer membership.
        user_to_membership = form.cleaned_data.get('user_to')
        building = self.get_object().building
        # Assign new user as main administrator.
        building.created_by = user_to_membership.user
        building.save()

        messages.success(
            self.request,
            _('Su membresía ha sido transferida exitosamente'),
        )

        return redirect(
            'buildings:memberships_list',
            self.get_object().building.id,
        )
