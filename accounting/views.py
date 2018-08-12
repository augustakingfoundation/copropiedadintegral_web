from django.views.generic import CreateView
from django.shortcuts import get_object_or_404

from buildings.models import Building
from accounting.models import Accounting
from accounting.forms import AccountingForm


class AccountingFormView(CreateView):
    """
    Account form view. Condominium administrator or
    accountant can create a new accountant assigned to a condo.
    This is a One to one relationship betweeen and accounting
    model and a condo, so and accounting model for a condo only
    can be created once.
    """
    model = Accounting
    form_class = AccountingForm
    template_name = 'accounting_form.html'

    def get_object(self, queryset=None):
        return get_object_or_404(
            Building,
            pk=self.kwargs['building_id'],
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['building'] = self.get_object()

        return context
