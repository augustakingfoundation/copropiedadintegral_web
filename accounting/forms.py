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
    coefficient = forms.DecimalField(
        max_value=0,
        min_value=100,
        label=_('coeficiente'),
    )

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

    def clean_coefficient(self):
        # Validation to the coefficient field. It must
        # be a value between 0 and 100.
        value = self.cleaned_data['coefficient']

        if value:
            if value < 0 or value > 100:
                raise forms.ValidationError(
                    _('El coeficiente debe ser un valor '
                      'entre 0 y 100')
                )

        return value
