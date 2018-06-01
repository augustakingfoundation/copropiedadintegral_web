from django.views.generic import CreateView
from django.views.generic import DetailView
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.shortcuts import redirect

from app.mixins import CustomUserMixin
from .models import Building
from .models import BuildingMembership
from .forms import BuildingForm
from .permissions import BuildingPermissions


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
    template_name = 'buildings/building_detail.html'

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
