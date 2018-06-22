from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic import UpdateView

from .forms import BuildingForm
from .forms import LeaseholderFormSet
from .forms import OwnerFormSet
from .forms import UnitForm
from .forms import ParkingLotForm
from .models import Building
from .models import BuildingMembership
from .models import Leaseholder
from .models import Owner
from .models import ParkingLot
from .models import Unit
from .permissions import BuildingPermissions
from app.mixins import CustomUserMixin


class BuildingFormView(CustomUserMixin, CreateView):
    """
    Form view to create a new Building or condo.
    A membership with administrator role is created
    to the authenticated user.
    """
    model = Building
    form_class = BuildingForm
    template_name = 'buildings/building_form.html'

    def test_func(self):
        return BuildingPermissions.can_create_building(
            user=self.request.user,
        )

    @transaction.atomic
    def form_valid(self, form):
        building = form.save(commit=False)
        building.created_by = self.request.user
        building.save()

        BuildingMembership.objects.create(
            user=self.request.user,
            building=building,
            is_administrator=True,
            is_active=True,
        )

        messages.success(
            self.request,
            _('Copropiedad creada exitosamente.')
        )

        return redirect(building.get_absolute_url())


class BuildingDetailView(CustomUserMixin, DetailView):
    """
    Detail view of a building or condo.
    """
    model = Building
    template_name = 'buildings/administrative/building_detail.html'

    def get_object(self, queryset=None):
        return get_object_or_404(
            Building,
            pk=self.kwargs['pk'],
        )

    def test_func(self):
        return BuildingPermissions.can_view_building_detail(
            user=self.request.user,
            building=self.get_object(),
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_edit_building'] = BuildingPermissions.can_edit_building(
            user=self.request.user,
            building=self.get_object(),
        )

        context['active_general'] = True

        return context


class BuildingUpdateView(CustomUserMixin, UpdateView):
    """
    Form view to update basic information about a building
    or condo.
    """
    model = Building
    form_class = BuildingForm
    template_name = 'buildings/building_form.html'

    def test_func(self):
        return BuildingPermissions.can_edit_building(
            user=self.request.user,
            building=self.get_object(),
        )

    def get_object(self, queryset=None):
        building = get_object_or_404(
            Building,
            pk=self.kwargs['pk'],
        )

        return building

    def get_success_url(self):
        return reverse(
            'buildings:building_detail', args=[self.kwargs['pk']]
        )

    @transaction.atomic
    def form_valid(self, form):
        form.save()

        messages.success(
            self.request,
            _('Copropiedad actualizada correctamente.'),
        )

        return super().form_valid(form)


class UnitsListView(CustomUserMixin, ListView):
    """
    List view with the units (apartments, houses or offices)
    created in a building or condo.
    """
    model = Unit
    template_name = 'buildings/administrative/units_list.html'
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

        return context


class UnitFormView(CustomUserMixin, TemplateView):
    """
    Form view to create a unit (apartment, house, office).
    Two formset are processed in this view. A formset to
    add multiple owners, and a formset to add multiple
    leaseholders.
    """
    template_name = 'buildings/administrative/unit_form.html'

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

        return self.process_data(form, owner_formset, leaseholder_formset)

    @transaction.atomic
    def process_data(self, form, owner_formset, leaseholder_formset):
        # Save unit form data.
        unit = form.save(commit=False)
        unit.building = self.get_object()
        unit.save()

        # Create Owner instances.
        for owner_form in owner_formset:
            if owner_form.is_valid():
                owner = owner_form.save(commit=False)
                owner.unit = unit
                owner.save()

        # Create Leaseholder instances.
        for leaseholder_form in leaseholder_formset:
            if leaseholder_form.is_valid():
                leaseholder = leaseholder_form.save(commit=False)
                leaseholder.unit = unit
                leaseholder.save()

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
    template_name = 'buildings/administrative/unit_form.html'

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

        return self.process_data(form, owner_formset, leaseholder_formset)

    @transaction.atomic
    def process_data(self, form, owner_formset, leaseholder_formset):
        unit = form.save()

        # Update, delete or create new Owner instances for this unit.
        for owner_form in owner_formset:
            if owner_form.is_valid():
                owner = owner_form.save(commit=False)
                owner.unit = unit
                owner.save()

                delete = owner_form.cleaned_data['DELETE']

                if delete:
                    owner.delete()

        # Update, delete or create new Leaseholder instances for this unit.
        for leaseholder_form in leaseholder_formset:
            if leaseholder_form.is_valid():
                leaseholder = leaseholder_form.save(commit=False)
                leaseholder.unit = unit
                leaseholder.save()

                delete = leaseholder_form.cleaned_data['DELETE']

                if delete:
                    leaseholder.delete()

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
    template_name = 'buildings/administrative/unit_detail.html'

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


class ParkingLotFormView(CustomUserMixin, CreateView):
    """
    Form view to create a new parking lot of a unit.
    """
    model = ParkingLot
    form_class = ParkingLotForm
    template_name = 'buildings/administrative/parkinglot_form.html'

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
    template_name = 'buildings/administrative/parkinglot_form.html'

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
        context['active_units'] = True

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
