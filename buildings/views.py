from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.views.generic import TemplateView
from django.views.generic import DetailView
from django.views.generic import UpdateView
from django.views.generic import ListView
from django.urls import reverse

from .forms import BuildingForm
from .forms import UnitForm
from .forms import OwnerFormSet
from .models import Building
from .models import BuildingMembership
from .models import Unit
from .models import Owner
from .permissions import BuildingPermissions
from app.mixins import CustomUserMixin


class BuildingFormView(CustomUserMixin, CreateView):
    model = Building
    form_class = BuildingForm
    template_name = 'buildings/building_form.html'

    def test_func(self):
        return BuildingPermissions.can_create_building(
            user=self.request.user,
        )

    @transaction.atomic
    def form_valid(self, form):
        building = form.save()

        BuildingMembership.objects.create(
            user=self.request.user,
            building=building,
            is_administrator=True,
            is_active=True,
        )

        messages.success(
            self.request,
            'Copropiedad creada exitosamente.'
        )

        return redirect(building.get_absolute_url())


class BuildingDetailView(CustomUserMixin, DetailView):
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
            'Copropiedad actualizada correctamente.',
        )

        return super().form_valid(form)


class UnitsListView(CustomUserMixin, ListView):
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

    def get(self, *args, **kwargs):
        form = UnitForm()
        formset = OwnerFormSet(queryset=Owner.objects.none())

        return self.render_to_response(
            self.get_context_data(form=form, formset=formset)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['building'] = self.get_object()
        context['active_units'] = True
        return context

    @transaction.atomic
    def form_valid(self, form):
        unit = form.save(commit=False)
        unit.building = self.get_object()
        unit.save()

        messages.success(
            self.request,
            'Unidad creada exitosamente.'
        )

        return redirect(unit.get_absolute_url())


class UnitDetailView(CustomUserMixin, DetailView):
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
        context['can_edit_unit'] = BuildingPermissions.can_edit_unit(
            user=self.request.user,
            building=self.get_object().building,
        )

        return context


class UnitUpdateView(CustomUserMixin, UpdateView):
    model = Unit
    form_class = UnitForm
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

    def get_success_url(self):
        return reverse(
            'buildings:unit_detail', args=[
                self.kwargs['b_pk'],
                self.kwargs['u_pk'],
            ]
        )

    @transaction.atomic
    def form_valid(self, form):
        form.save()

        messages.success(
            self.request,
            'Unidad actualizada correctamente.',
        )

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_units'] = True
        context['building'] = self.get_object().building
        context['unit_update'] = True

        return context
