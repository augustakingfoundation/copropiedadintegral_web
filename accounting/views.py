from django.views.generic import TemplateView


class AccountingFormView(TemplateView):
    """
    Account form view. Condominium administrator or
    accountant can create a new accountant assigned to a condo.
    This is a One to one relationship betweeen and accounting
    model and a condo, so and accounting model for a condo only
    can be created once.
    """
    template_name = 'accounting_form.html'
