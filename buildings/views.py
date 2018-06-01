from django.views.generic import CreateView
from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect

from app.mixins import CustomUserMixin
from .models import Building
from .forms import BuildingForm
from .permissions import BuildingPermissions


class BuildingFormView(CustomUserMixin, CreateView):
    model = Building
    form_class = BuildingForm
    template_name = 'Buildings/building_form.html'

    def test_func(self):
        return BuildingPermissions.can_create_building(
            user=self.request.user,
        )

    @transaction.atomic
    def form_valid(self, form):
        building = form.save(commit=False)

        messages.success(
            self.request,
            'Copropiedad creada exitosamente.'
        )

        return redirect(building.get_absolute_url())
