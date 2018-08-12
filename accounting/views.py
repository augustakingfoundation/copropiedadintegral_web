import xlrd

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
from accounting.models import EconomicActivity
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

    @transaction.atomic
    def form_valid(self, form):
        building = self.get_object()

        accounting = form.save(commit=False)
        accounting.condo = building
        accounting.save()

        return super().form_valid(form)


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

        # Read xls file to create economic activities instances.
        book = xlrd.open_workbook(file_contents=file.read())
        first_sheet = book.sheet_by_index(0)

        num_rows = first_sheet.nrows
        num_cols = first_sheet.ncols

        # Iterate all rows and columns to get the values.
        # Excel file must not have headers.
        # Column one is for economic activities codes.
        # Column two is for economic activities names.
        # Column three is for economic activities rates.
        for row_idx in range(0, num_rows):
            code = None
            name = None
            rate = None

            for col_idx in range(0, num_cols):
                cell = first_sheet.cell(row_idx, col_idx)

                if col_idx == 0:
                    code = int(cell.value)
                elif col_idx == 1:
                    name = cell.value
                elif col_idx == 2:
                    rate = cell.value
                    rate = float(rate.replace('%', '').replace(',', '.'))

            if code and name and rate:
                if not EconomicActivity.objects.filter(
                    code=code,
                ):
                    EconomicActivity.objects.create(
                        code=code,
                        name=name,
                        rate=rate,
                    )

        messages.success(
            self.request,
            _('Actividades económicas actualizadas.'),
        )

        return super().form_valid(form)
