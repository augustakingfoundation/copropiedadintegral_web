from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.utils.translation import ugettext as _
from django.views.generic import View
from django.shortcuts import redirect
from django.db import transaction

from app.mixins import CustomUserMixin
from buildings.forms import ConfirmOwnerUpdateFormSet
from buildings.models import Building
from buildings.models import UnitDataUpdate
from buildings.permissions import BuildingPermissions


class DataUpdateView(CustomUserMixin, TemplateView):
    """
    Template view to manage data update module. Administrators
    and administrative assistants can request for data update
    from owners and leaseholders.
    """
    template_name = 'buildings/administrative/data_update/data_update.html'

    def test_func(self):
        return BuildingPermissions.can_edit_building(
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
        context['building'] = self.get_object()
        context['active_units'] = True

        owner_update_formset = ConfirmOwnerUpdateFormSet(
            prefix='owner_update',
            queryset=UnitDataUpdate.objects.filter(
                unit__building=self.get_object(),
            ),
        )

        context['owner_update_formset'] = owner_update_formset

        return context


class RequestOwnersUpdateView(CustomUserMixin, View):
    """
    View to manage the post request of the owners update formset.
    """
    def test_func(self):
        return BuildingPermissions.can_edit_building(
            user=self.request.user,
            building=self.get_object(),
        )

    def get_object(self, queryset=None):
        return get_object_or_404(
            Building,
            pk=self.kwargs['pk'],
        )

    @transaction.atomic
    def post(self, *args, **kwargs):
        # Get formset post data.
        owner_update_formset = ConfirmOwnerUpdateFormSet(
            self.request.POST,
            prefix='owner_update',
            queryset=UnitDataUpdate.objects.filter(
                unit__building=self.get_object(),
            ),
        )

        for form in owner_update_formset:
            if form.is_valid():
                unit_data_object = form.save(commit=False)

                # Get request value. If True, an email
                # will be sent to the unit registered owners.
                update = form.cleaned_data['update']

                if update and unit_data_object.unit.owner_has_email:
                    # Owners update form must be available.
                    unit_data_object.enable_owners_update = True
                    unit_data_object.save()

        messages.success(
            self.request,
            _('Se ha solicitado la actualización de datos a'
              ' los propietarios con correo electrónico registrado.')
        )

        return redirect(
            'buildings:data_update_view',
            self.get_object().id,
        )


class OwnersUpdateForm(TemplateView):
    """
    Owners update form. This form will be available only if
    administrators have enabled the update post by requesting
    owners data update.
    """
    template_name = 'buildings/administrative/data_update/owners_update_form.html'

    def get_object(self, queryset=None):
        return get_object_or_404(
            UnitDataUpdate,
            enable_owners_update=True,
            pk=self.kwargs['pk'],
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['unit_data'] = self.get_object()

        return context
