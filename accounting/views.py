from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import ugettext as _
from django.views.generic import CreateView
from django.views.generic import FormView

from accounting.forms import AccountingForm
from accounting.forms import EconomicActivitiesForm
from accounting.models import Accounting
from accounting.permissions import AccountingPermissions
from app.mixins import CustomUserMixin
from buildings.models import Building


class AccountingFormView(CustomUserMixin, CreateView):
    """
    Accounting form view. Condominium administrator or
    accountant can create a new accountant assigned to a condo.
    This is a One to one relationship betweeen and accounting
    model and a condo, so and accounting model for a condo only
    can be created once.
    """
    model = Accounting
    form_class = AccountingForm
    template_name = 'accounting_form.html'

    def test_func(self):
        return AccountingPermissions.can_create_accounting(
            user=self.request.user,
            building=self.get_object(),
        )

    def get_object(self, queryset=None):
        return get_object_or_404(
            Building,
            pk=self.kwargs['building_id'],
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['building'] = self.get_object()

        return context


class EconomicActivitiesFormView(CustomUserMixin, FormView):
    """
    Economic activities form. This is the way to classify
    the economic activities by productive processes in
    Colombia. Each condo must to select one activity. This view
    is a form view to upload an excel file with the economic
    activities to create instances og the EconomicActivity
    model. Excel file must contain a column with the code,
    a column with the name and a column with the rate.
    """
    form_class = EconomicActivitiesForm
    template_name = 'economic_activities_form.html'
    success_url = reverse_lazy('accounting:economic_activities_form')

    def test_func(self):
        return AccountingPermissions.can_change_economic_activities(
            user=self.request.user,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_economic_activities'] = True

        return context

    @transaction.atomic
    def form_valid(self, form):
        file = form.cleaned_data['excel_file']

        print("file")
        print(file)

        messages.success(
            self.request,
            _('Actividades económicas actualizadas.'),
        )

        return super().form_valid(form)
