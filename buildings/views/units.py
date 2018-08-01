from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import TemplateView

from app.mixins import CustomUserMixin
from buildings.forms import LeaseholderFormSet
from buildings.forms import OwnerFormSet
from buildings.forms import UnitForm
from buildings.models import Building
from buildings.models import Leaseholder
from buildings.models import Owner
from buildings.models import Unit
from buildings.models import UnitDataUpdate
from buildings.permissions import BuildingPermissions
from buildings.utils import process_unit_formset
from buildings.utils import validate_is_main_formset


class UnitsListView(CustomUserMixin, ListView):
    """
    List view with the units (apartments, houses or offices)
    created in a building or condo.
    """
    model = Unit
    template_name = 'buildings/administrative/units/units_list.html'
    context_object_name = 'units_list'

    def test_func(self):
        return BuildingPermissions.can_view_units_list(
            user=self.request.user,
            building=self.get_object(),
        )

    def get_object(self, queryset=None):
        return get_object_or_404(
            Building,
            pk=self.kwargs['pk'],
        )

    def get_queryset(self):
        return Unit.objects.filter(building=self.get_object())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['building'] = self.get_object()
        context['active_units'] = True
        context['can_create_unit'] = BuildingPermissions.can_create_unit(
            user=self.request.user,
            building=self.get_object(),
        )

        context['can_view_unit_detail'] = BuildingPermissions.can_view_unit_detail(
            user=self.request.user,
            building=self.get_object(),
        )

        context['can_view_update_menu'] = BuildingPermissions.can_edit_building(
            user=self.request.user,
            building=self.get_object(),
        )

        return context


class UnitFormView(CustomUserMixin, TemplateView):
    """
    Form view to create a unit (apartment, house, office).
    Two formset are processed in this view. A formset to
    add multiple owners, and a formset to add multiple
    leaseholders.
    """
    template_name = 'buildings/administrative/units/unit_form.html'

    def test_func(self):
        return BuildingPermissions.can_create_unit(
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
        return context

    def get(self, *args, **kwargs):
        form = UnitForm()

        # Owner formset. Multiple owners can
        # be added to a unit.
        owner_formset = OwnerFormSet(
            prefix='owner',
            queryset=Owner.objects.none(),
        )

        # Leaseholders formset. Multiple owners can
        # be added to a unit.
        leaseholder_formset = LeaseholderFormSet(
            prefix='leaseholder',
            queryset=Leaseholder.objects.none(),
        )

        return self.render_to_response(
            self.get_context_data(
                form=form,
                owner_formset=owner_formset,
                leaseholder_formset=leaseholder_formset,
            )
        )

    @transaction.atomic
    def post(self, *args, **kwargs):
        form = UnitForm(self.request.POST)

        owner_formset = OwnerFormSet(
            self.request.POST,
            prefix='owner',
            queryset=Owner.objects.none(),
        )

        leaseholder_formset = LeaseholderFormSet(
            self.request.POST,
            prefix='leaseholder',
            queryset=Leaseholder.objects.none(),
        )

        # Check if unit form, owners formset and
        # leaseholders formset are valid. If not,
        # error messages are returned to the user.
        # It the forms are valid, the data will be
        # processed by the 'process_data' function.
        if (
            not form.is_valid() or
            not owner_formset.is_valid() or
            not leaseholder_formset.is_valid()
        ):
            return self.render_to_response(
                self.get_context_data(
                    form=form,
                    owner_formset=owner_formset,
                    leaseholder_formset=leaseholder_formset,
                )
            )

        # Validate the number of form with 'is_main' field
        # checked. If there are not forms checked or there
        # are more than one, an error message must be raised.
        #  Units must have one main owner.
        form, owner_formset, is_main_owner_counter = validate_is_main_formset(
            form=form,
            formset=owner_formset,
            formset_type='owner',
        )

        # Validate the number of form with 'is_main' field
        # checked. If there  are more than one, an error
        # message must be raised. Units must have only one
        # main leaseholder.
        form, leaseholder_formset, is_main_leaseholder_counter = validate_is_main_formset(
            form=form,
            formset=leaseholder_formset,
            formset_type='leaseholder',
        )

        # Return formsets errors.
        if (
            not is_main_owner_counter or
            is_main_owner_counter > 1 or
            is_main_leaseholder_counter > 1
        ):
            return self.render_to_response(
                self.get_context_data(
                    form=form,
                    owner_formset=owner_formset,
                    leaseholder_formset=leaseholder_formset,
                )
            )

        # Save unit form data.
        unit = form.save(commit=False)
        unit.building = self.get_object()
        unit.save()

        UnitDataUpdate.objects.create(unit=unit)

        # Create Owner instances.
        process_unit_formset(owner_formset, unit)

        # Process leaseholders formset only if
        # owners are not residents of the unit.
        if not unit.owner_set.filter(is_resident=True):
            # Create Leaseholder instances.
            process_unit_formset(leaseholder_formset, unit)

        messages.success(
            self.request,
            _('Unidad creada exitosamente.')
        )

        return redirect(unit.get_absolute_url())


class UnitUpdateView(CustomUserMixin, TemplateView):
    """
    Form view to update a unit. Owners formset and
    Leaseholders formset are available in this form view.
    Instanes created of the Owner model and of the
    Leaseholder model will be initialized in the formsets
    to update them easily.
    """
    template_name = 'buildings/administrative/units/unit_form.html'

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

    def get(self, *args, **kwargs):
        unit = self.get_object()

        form = UnitForm(instance=unit)

        # Owners formset. The instances of the Owner model
        # linked to the unit are passed in the 'queryset'
        # value.
        owner_formset = OwnerFormSet(
            prefix='owner',
            queryset=Owner.objects.filter(unit=unit),
        )

        # Leaseholders formset. The instances of the Leaseholder
        # model linked to the unit are passed in the 'queryset'
        # value.
        leaseholder_formset = LeaseholderFormSet(
            prefix='leaseholder',
            queryset=Leaseholder.objects.filter(unit=unit),
        )

        return self.render_to_response(
            self.get_context_data(
                form=form,
                owner_formset=owner_formset,
                leaseholder_formset=leaseholder_formset,
                object=self.get_object(),
            )
        )

    def post(self, *args, **kwargs):
        unit = self.get_object()

        form = UnitForm(
            self.request.POST,
            instance=unit,
        )
        owner_formset = OwnerFormSet(
            self.request.POST,
            prefix='owner',
            queryset=Owner.objects.filter(unit=unit),
        )
        leaseholder_formset = LeaseholderFormSet(
            self.request.POST,
            prefix='leaseholder',
            queryset=Leaseholder.objects.filter(unit=unit),
        )

        # Check if unit form, owners formset and
        # leaseholders formset are valid. If not,
        # error messages are returned to the user.
        # It the forms are valid, the data will be
        # processed by the 'process_data' function.
        if (
            not form.is_valid() or
            not owner_formset.is_valid() or
            not leaseholder_formset.is_valid()
        ):
            return self.render_to_response(
                self.get_context_data(
                    form=form,
                    owner_formset=owner_formset,
                    leaseholder_formset=leaseholder_formset,
                )
            )

        # Validate the number of form with 'is_main' field
        # checked. If there are not forms checked or there
        # are more than one, an error message must be raised.
        #  Units must have one main owner.
        form, owner_formset, is_main_owner_counter = validate_is_main_formset(
            form=form,
            formset=owner_formset,
            formset_type='owner',
        )

        # Validate the number of form with 'is_main' field
        # checked. If there  are more than one, an error
        # message must be raised. Units must have only one
        # main leaseholder.
        form, leaseholder_formset, is_main_leaseholder_counter = validate_is_main_formset(
            form=form,
            formset=leaseholder_formset,
            formset_type='leaseholder',
        )

        # Return formsets errors.
        if (
            not is_main_owner_counter or
            is_main_owner_counter > 1 or
            is_main_leaseholder_counter > 1
        ):
            return self.render_to_response(
                self.get_context_data(
                    form=form,
                    owner_formset=owner_formset,
                    leaseholder_formset=leaseholder_formset,
                )
            )

        # Save unit form data.
        unit = form.save()
        # Update, delete or create new Owner instances for this unit.
        process_unit_formset(owner_formset, unit)

        # Process leaseholders formset only if
        # owners are not residents of the unit.
        if not unit.owner_set.filter(is_resident=True):
            # Update, delete or create new Leaseholder instances for this unit.
            process_unit_formset(leaseholder_formset, unit)

        messages.success(
            self.request,
            _('Unidad actualizada correctamente.'),
        )

        return redirect(unit.get_absolute_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_units'] = True
        context['building'] = self.get_object().building
        context['unit_update'] = True

        return context


class UnitDetailView(CustomUserMixin, DetailView):
    """
    Detail view of a Unit (Apartment, house or office).
    """
    model = Building
    template_name = 'buildings/administrative/units/unit_detail.html'

    def get_object(self, queryset=None):
        return get_object_or_404(
            Unit,
            building_id=self.kwargs['b_pk'],
            pk=self.kwargs['u_pk'],
        )

    def test_func(self):
        return BuildingPermissions.can_view_unit_detail(
            user=self.request.user,
            building=self.get_object().building,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_units'] = True
        context['building'] = self.get_object().building

        # Permission to allow users to edit a unit.
        context['can_edit_unit'] = BuildingPermissions.can_edit_unit(
            user=self.request.user,
            building=self.get_object().building,
        )

        return context


class UnitDeleteView(CustomUserMixin, DeleteView):
    """
    Unit delete view. Users are redirected to a view
    in which they will be asked about confirmation for
    delete a unit definitely.
    """
    model = Unit
    template_name = 'buildings/administrative/units/unit_delete_confirm.html'

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

    def get_success_url(self):
        # Reverse to units list view.
        return reverse(
            'buildings:units_list',
            args=[self.kwargs['b_pk']]
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Returned to activate the correct tab in the side bar.
        context['active_units'] = True
        context['building'] = self.get_object().building

        return context

    def delete(self, request, *args, **kwargs):
        messages.success(
            self.request,
            _('Unidad eliminado exitosamente.')
        )

        return super().delete(request, *args, **kwargs)
