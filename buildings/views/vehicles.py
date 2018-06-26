from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from django.views.generic import CreateView

from app.mixins import CustomUserMixin
from buildings.forms import VehicleForm
from buildings.models import Unit
from buildings.models import Vehicle
from buildings.permissions import BuildingPermissions


class VehicleFormView(CustomUserMixin, CreateView):
    """
    Form view to register a new vehicle into a unit.
    """
    model = Vehicle
    form_class = VehicleForm
    template_name = 'buildings/administrative/vehicle_form.html'

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
        context['active_units'] = True

        return context

    @transaction.atomic
    def form_valid(self, form):
        # Get unit instance.
        unit = self.get_object()
        # Create parking lot object.
        vehicle = form.save(commit=False)
        vehicle.unit = self.get_object()
        vehicle.save()

        messages.success(
            self.request,
            _('Vehículo creado exitosamente.')
        )

        return redirect(unit.get_absolute_url())
