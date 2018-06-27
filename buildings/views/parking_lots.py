from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic.edit import DeleteView

from app.mixins import CustomUserMixin
from buildings.forms import ParkingLotForm
from buildings.models import ParkingLot
from buildings.models import Unit
from buildings.permissions import BuildingPermissions


class ParkingLotFormView(CustomUserMixin, CreateView):
    """
    Form view to create a new parking lot of a unit.
    """
    model = ParkingLot
    form_class = ParkingLotForm
    template_name = 'buildings/administrative/parking_lots/parkinglot_form.html'

    def test_func(self):
        return BuildingPermissions.can_edit_unit(
            user=self.request.user,
            building=self.get_object().building,
        )

    def get_object(self, queryset=None):
        return get_object_or_404(
            Unit,
            building_id=self.kwargs['b_pk'],
            pk=self.kwargs['u_pk'],
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['unit'] = self.get_object()
        context['building'] = self.get_object().building
        # Returned to activate the correct tab in the side bar.
        context['active_units'] = True

        return context

    @transaction.atomic
    def form_valid(self, form):
        # Get unit instance.
        unit = self.get_object()
        # Create parking lot object.
        parking_lot = form.save(commit=False)
        parking_lot.unit = self.get_object()
        parking_lot.save()

        messages.success(
            self.request,
            _('Parqueadero creado exitosamente.')
        )

        return redirect(unit.get_absolute_url())


class ParkingLotUpdateView(CustomUserMixin, UpdateView):
    """
    Form view to update information about a parking lot.
    """
    model = ParkingLot
    form_class = ParkingLotForm
    template_name = 'buildings/administrative/parking_lots/parkinglot_form.html'

    def test_func(self):
        return BuildingPermissions.can_edit_unit(
            user=self.request.user,
            building=self.get_object().unit.building,
        )

    def get_object(self, queryset=None):
        # Get parking lot object.
        return get_object_or_404(
            ParkingLot,
            unit_id=self.kwargs['u_pk'],
            pk=self.kwargs['p_pk'],
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['unit'] = self.get_object().unit
        context['building'] = self.get_object().unit.building
        # Returned to activate the correct tab in the side bar.
        context['active_units'] = True
        # Returned to put the correct title in the parking lot form.
        context['parking_lot_update'] = True

        return context

    def get_success_url(self):
        # Reverse to unit detail.
        return reverse(
            'buildings:unit_detail',
            args=[self.kwargs['b_pk'], self.kwargs['u_pk']]
        )

    @transaction.atomic
    def form_valid(self, form):
        # Update parking lot object.
        form.save()

        messages.success(
            self.request,
            _('Parqueadero actualizado exitosamente.'),
        )

        return super().form_valid(form)


class ParkingLotDeleteView(CustomUserMixin, DeleteView):
    """
    Parking lot delete view. Users are redirected to a view
    in which they will be asked about confirmation for
    delete a parking lot definitely.
    """
    model = ParkingLot
    template_name = 'buildings/administrative/parking_lots/parking_lot_delete_confirm.html'

    def test_func(self):
        return BuildingPermissions.can_edit_unit(
            user=self.request.user,
            building=self.get_object().unit.building,
        )

    def get_object(self, queryset=None):
        # Get parking lot object.
        return get_object_or_404(
            ParkingLot,
            unit_id=self.kwargs['u_pk'],
            pk=self.kwargs['p_pk'],
        )

    def get_success_url(self):
        # Reverse to unit detail.
        return reverse(
            'buildings:unit_detail',
            args=[self.kwargs['b_pk'], self.kwargs['u_pk']]
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['unit'] = self.get_object().unit
        # Returned to activate the correct tab in the side bar.
        context['active_units'] = True
        context['building'] = self.get_object().unit.building

        return context
