from django import forms
from django.utils.translation import gettext_lazy as _

from accounting.models import Accounting


RATE_CHOICES = (
    (0.3, '0.3'),
    (0.4, '0.4'),
    (0.6, '0.6'),
    (1.5, '1.5'),
    (1.6, '1.6'),
)


class AccountingForm(forms.ModelForm):
    """
    Form to create the accounting model of a condominium.
    """
    rate = forms.ChoiceField(
        label=_('tarifa'),
        choices=RATE_CHOICES,
    )

    class Meta:
        model = Accounting
        fields = (
            'initial_period',
            'economic_activity',
            'apply_retention',
            'is_self_withholding',
            'rate',
            'nit_dian',
            'local_nit_dian',
        )
