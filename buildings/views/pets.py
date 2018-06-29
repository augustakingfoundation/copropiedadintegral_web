from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from django.views.generic import CreateView
from django.views.generic import DetailView

from app.mixins import CustomUserMixin
from buildings.forms import PetForm
from buildings.models import Pet
from buildings.models import Unit
from buildings.permissions import BuildingPermissions


class PetFormView(CustomUserMixin, CreateView):
    """
    Form view to register a new pet into a unit.
    """
    model = Pet
    form_class = PetForm
    template_name = 'buildings/administrative/pets/pet_form.html'

    def test_func(self):
        return BuildingPermissions.can_edit_unit(
            user=self.request.user,
            building=self.get_object().building,
        )

    def get_object(self, queryset=None):
        # Get unit object.
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
        # Create pet object.
        pet = form.save(commit=False)
        pet.unit = self.get_object()
        pet.save()

        messages.success(
            self.request,
            _('Mascota creada exitosamente.')
        )

        return redirect(unit.get_absolute_url())


class PetDetailView(CustomUserMixin, DetailView):
    """
    Detail view of a pet registered into an unit.
    """
    model = Pet
    template_name = 'buildings/administrative/pets/pet_detail.html'

    def get_object(self, queryset=None):
        return get_object_or_404(
            Pet,
            pk=self.kwargs['pet_pk'],
        )

    def test_func(self):
        return BuildingPermissions.can_edit_unit(
            user=self.request.user,
            building=self.get_object().unit.building,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['unit'] = self.get_object().unit
        context['building'] = self.get_object().unit.building
        # Returned to activate the correct tab in the side bar.
        context['active_units'] = True

        return context
