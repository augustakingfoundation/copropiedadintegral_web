from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.views.generic import CreateView
from django.views.generic import DetailView

from app.mixins import CustomUserMixin
from buildings.forms import BuildingForm
from buildings.models import Building
from buildings.models import BuildingMembership
from buildings.permissions import BuildingPermissions
from django.views.generic import UpdateView


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
