from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DetailView
from django.views.generic import TemplateView
from django.views.generic.edit import DeleteView
from django.urls import reverse

from app.mixins import CustomUserMixin
from buildings.forms import ResidentForm
from buildings.forms import EmergencyContactFormSet
from buildings.utils import process_emergency_contacts_formset
from buildings.models import Resident
from buildings.models import Unit
from buildings.models import EmergencyContact
from buildings.permissions import BuildingPermissions


class ResidentFormView(CustomUserMixin, TemplateView):
    template_name = 'buildings/administrative/residents/resident_form.html'
    form_class = ResidentForm

    def test_func(self):
        return BuildingPermissions.can_edit_unit(
            user=self.request.user,
            building=self.get_object().building,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['unit'] = self.get_object()
        context['building'] = self.get_object().building
        # Returned to activate the correct tab in the side bar.
        context['active_units'] = True

        return context

    def get_object(self, queryset=None):
        return get_object_or_404(
            Unit,
            building_id=self.kwargs['b_pk'],
            pk=self.kwargs['u_pk'],
        )

    def get(self, *args, **kwargs):
        # Resident form.
        form = ResidentForm()
        # Emergency contacts formset.
        formset = EmergencyContactFormSet(
            queryset=EmergencyContact.objects.none(),
        )

        return self.render_to_response(
            self.get_context_data(form=form, formset=formset)
        )

    @transaction.atomic
    def post(self, *args, **kwargs):
        # Resident form.
        form = ResidentForm(self.request.POST)
        # Emergency contacts formset.
        formset = EmergencyContactFormSet(
            self.request.POST,
            queryset=EmergencyContact.objects.none(),
        )

        if not form.is_valid() or not formset.is_valid():
            return self.render_to_response(
                self.get_context_data(form=form, formset=formset)
            )

        unit = self.get_object()

        # Create resident instance.
        resident = form.save(commit=False)
        resident.unit = unit
        resident.save()

        # Create emergency contact instances.
        process_emergency_contacts_formset(formset, resident)

        messages.success(
            self.request,
            _('Residente creado exitosamente.')
        )

        return redirect(resident.get_absolute_url())


class ResidentDetailView(CustomUserMixin, DetailView):
    """
    Detail view of a resident registered into a unit.
    """
    model = Resident
    template_name = 'buildings/administrative/residents/resident_detail.html'

    def get_object(self, queryset=None):
        return get_object_or_404(
            Resident,
            pk=self.kwargs['r_pk'],
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


class ResidentUpdateView(CustomUserMixin, TemplateView):
    template_name = 'buildings/administrative/residents/resident_form.html'
    form_class = ResidentForm

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

    def get_object(self, queryset=None):
        return get_object_or_404(
            Resident,
            unit_id=self.kwargs['u_pk'],
            id=self.kwargs['r_pk'],
        )

    def get(self, *args, **kwargs):
        resident = self.get_object()
        # Resident form.
        form = ResidentForm(instance=resident)
        # Emergency contacts formset.
        formset = EmergencyContactFormSet(
            queryset=EmergencyContact.objects.filter(resident=resident),
        )

        return self.render_to_response(
            self.get_context_data(form=form, formset=formset)
        )

    @transaction.atomic
    def post(self, *args, **kwargs):
        # Resident form.
        form = ResidentForm(
            self.request.POST,
            instance=self.get_object(),
        )
        # Emergency contacts formset.
        formset = EmergencyContactFormSet(
            self.request.POST,
            queryset=EmergencyContact.objects.filter(
                resident=self.get_object(),
            ),
        )

        if not form.is_valid() or not formset.is_valid():
            return self.render_to_response(
                self.get_context_data(form=form, formset=formset)
            )

        resident = form.save()

        # Update emergency contact instances.
        process_emergency_contacts_formset(formset, resident)

        messages.success(
            self.request,
            _('Residente actualizado exitosamente.')
        )

        return redirect(resident.get_absolute_url())
