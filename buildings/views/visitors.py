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
from buildings.forms import VisitorForm
from buildings.models import Unit
from buildings.models import Visitor
from buildings.permissions import BuildingPermissions


class VisitorFormView(CustomUserMixin, CreateView):
    """
    Form view to register a new authorized visitor into a unit.
    """
    model = Visitor
    form_class = VisitorForm
    template_name = 'buildings/administrative/visitors/visitor_form.html'

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
        # Create authorized visitor object.
        visitor = form.save(commit=False)
        visitor.unit = self.get_object()
        visitor.save()

        messages.success(
            self.request,
            _('Visitante creado exitosamente.')
        )

        return redirect(unit.get_absolute_url())


class VisitorUpdateView(CustomUserMixin, UpdateView):
    """
    Form view to update information about an authorized visitor.
    """
    model = Visitor
    form_class = VisitorForm
    template_name = 'buildings/administrative/visitors/visitor_form.html'

    def test_func(self):
        return BuildingPermissions.can_edit_unit(
            user=self.request.user,
            building=self.get_object().unit.building,
        )

    def get_object(self, queryset=None):
        # Get vehicle object.
        return get_object_or_404(
            Visitor,
            unit_id=self.kwargs['u_pk'],
            pk=self.kwargs['av_pk'],
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['unit'] = self.get_object().unit
        context['building'] = self.get_object().unit.building
        # Returned to activate the correct tab in the side bar.
        context['active_units'] = True
        # Returned to put the correct title in the visitor form.
        context['visitor_update'] = True

        return context

    def get_success_url(self):
        # Reverse to unit detail.
        return reverse(
            'buildings:unit_detail',
            args=[self.kwargs['b_pk'], self.kwargs['u_pk']]
        )

    @transaction.atomic
    def form_valid(self, form):
        # Update visitor object.
        form.save()

        messages.success(
            self.request,
            _('Visitante actualizado exitosamente.'),
        )

        return super().form_valid(form)


class VisitorDeleteView(CustomUserMixin, DeleteView):
    """
    Authorized visitor delete view. Users are redirected to a view
    in which they will be asked about confirmation for
    delete a visitor definitely.
    """
    model = Visitor
    template_name = 'buildings/administrative/visitors/visitor_delete_confirm.html'

    def test_func(self):
        return BuildingPermissions.can_edit_unit(
            user=self.request.user,
            building=self.get_object().unit.building,
        )

    def get_object(self, queryset=None):
        # Get vehicle object.
        return get_object_or_404(
            Visitor,
            unit_id=self.kwargs['u_pk'],
            pk=self.kwargs['av_pk'],
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

    def delete(self, request, *args, **kwargs):
        messages.success(
            self.request,
            _('Visitante eliminado exitosamente.')
        )

        return super().delete(request, *args, **kwargs)
