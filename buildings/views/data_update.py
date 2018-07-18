from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from app.mixins import CustomUserMixin
from buildings.forms import ConfirmOwnerUpdateFormSet
from buildings.models import Building
from buildings.models import UnitDataUpdate
from buildings.permissions import BuildingPermissions


class DataUpdateView(CustomUserMixin, TemplateView):
    """
    """
    template_name = 'buildings/administrative/data_update/data_update.html'

    def test_func(self):
        return BuildingPermissions.can_edit_building(
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

        owner_update_formset = ConfirmOwnerUpdateFormSet(
            prefix='owner',
            queryset=UnitDataUpdate.objects.filter(
                unit__building=self.get_object(),
            ),
        )

        context['owner_update_formset'] = owner_update_formset

        return context
