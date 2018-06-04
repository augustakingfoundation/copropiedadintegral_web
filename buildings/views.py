from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import UpdateView
from django.urls import reverse

from .forms import BuildingForm
from .models import Building
from .models import BuildingMembership
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
        building = get_object_or_404(
            Building,
            pk=self.kwargs['pk'],
        )

        return building

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
