from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic.edit import DeleteView
from django.urls import reverse

from app.mixins import CustomUserMixin
from buildings.models import DomesticWorker
from buildings.models import Unit
from buildings.forms import DomesticWorkerForm
from buildings.permissions import BuildingPermissions


class DomesticWorkerFormView(CustomUserMixin, CreateView):
    """
    Form view to register a new vehicle into a unit.
    """
    model = DomesticWorker
    form_class = DomesticWorkerForm
    template_name = 'buildings/administrative/domesticworker_form.html'

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
        # Create domestic worker object.
        domestic_worker = form.save(commit=False)
        domestic_worker.unit = self.get_object()
        domestic_worker.save()

        messages.success(
            self.request,
            _('Trabajador doméstico creado exitosamente.')
        )

        return redirect(unit.get_absolute_url())


class DomesticWorkerUpdateView(CustomUserMixin, UpdateView):
    """
    Form view to update information about a domestic worker.
    """
    model = DomesticWorker
    form_class = DomesticWorkerForm
    template_name = 'buildings/administrative/domesticworker_form.html'

    def test_func(self):
        return BuildingPermissions.can_edit_unit(
            user=self.request.user,
            building=self.get_object().unit.building,
        )

    def get_object(self, queryset=None):
        # Get domestic worker object.
        return get_object_or_404(
            DomesticWorker,
            unit_id=self.kwargs['u_pk'],
            pk=self.kwargs['dw_pk'],
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['unit'] = self.get_object().unit
        context['building'] = self.get_object().unit.building
        context['active_units'] = True
        context['domestic_worker_update'] = True

        return context

    def get_success_url(self):
        # Reverse to unit detail.
        return reverse(
            'buildings:unit_detail',
            args=[self.kwargs['b_pk'], self.kwargs['u_pk']]
        )

    @transaction.atomic
    def form_valid(self, form):
        # Update domestic worker object.
        form.save()

        messages.success(
            self.request,
            _('Trabajador doméstico actualizado exitosamente.'),
        )

        return super().form_valid(form)
