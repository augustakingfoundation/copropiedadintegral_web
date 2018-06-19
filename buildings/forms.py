import re

from django import forms
from django.forms import modelformset_factory
from django.utils.translation import ugettext as _

from .data import BUILDING_DOCUMENT_TYPE_NIT
from .data import BUILDING_DOCUMENT_TYPE_CC
from .models import Building
from .models import Unit
from .models import Owner
from .models import Leaseholder


class BuildingForm(forms.ModelForm):
    class Meta:
        model = Building
        fields = (
            'name',
            'document_type',
            'document_number',
            'logo',
            'city',
            'address',
            'email',
            'mobile_phone',
            'phone_number',
            'initial_period',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].empty_label = _('Ciudad')

        fields = [
            'name',
            'document_number',
            'logo',
            'city',
            'address',
            'email',
            'mobile_phone',
            'phone_number',
            'initial_period',
        ]

        for field in fields:
            label = self.fields[field].label
            self.fields[field].label = ''
            self.fields[field].widget.attrs['placeholder'] = label

    def clean(self):
        cleaned_data = super().clean()
        document_type = cleaned_data.get('document_type')
        document_number = cleaned_data.get('document_number')

        if (
            document_type == BUILDING_DOCUMENT_TYPE_NIT and
            not re.match(r'^\d{5,15}-\d{1}$', document_number)
        ):
            self.add_error(
                'document_number',
                _('El NIT ingresado no es válido. Ej: 12345678-1'),
            )

        elif (
            document_type == BUILDING_DOCUMENT_TYPE_CC and
            not re.match(r'^\d{5,15}$', document_number)
        ):
            self.add_error(
                'document_number',
                _('El documento ingresado solo debe contener números'),
            )


class OwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = (
            'name',
            'last_name',
            'document_type',
            'document_number',
            'mobile_phone',
            'phone_number',
            'correspondence_address',
            'email',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        fields = [
            'name',
            'last_name',
            'document_type',
            'document_number',
            'mobile_phone',
            'phone_number',
            'correspondence_address',
            'email',
        ]

        for field in fields:
            label = self.fields[field].label
            self.fields[field].label = ''
            self.fields[field].widget.attrs['placeholder'] = label


OwnerFormSet = modelformset_factory(
    Owner,
    form=OwnerForm,
    extra=0,
    max_num=5,
    min_num=1,
    validate_min=True,
    can_delete=True,
)


class LeaseholderForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = (
            'name',
            'last_name',
            'document_type',
            'document_number',
            'mobile_phone',
            'phone_number',
            'email',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        fields = [
            'name',
            'last_name',
            'document_type',
            'document_number',
            'mobile_phone',
            'phone_number',
            'email',
        ]

        for field in fields:
            label = self.fields[field].label
            self.fields[field].label = ''
            self.fields[field].widget.attrs['placeholder'] = label


LeaseholderFormSet = modelformset_factory(
    Leaseholder,
    form=LeaseholderForm,
    extra=0,
    max_num=2,
    min_num=1,
    validate_min=False,
    can_delete=True,
)


class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = (
            'block',
            'unit',
            'area',
            'real_estate_registration',
            'coefficient',
            'observations',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        fields = [
            'block',
            'unit',
            'area',
            'real_estate_registration',
            'coefficient',
            'observations',
        ]

        for field in fields:
            label = self.fields[field].label
            self.fields[field].label = ''
            self.fields[field].widget.attrs['placeholder'] = label

    def clean_coefficient(self):
        value = self.cleaned_data['coefficient']

        if value:
            if value < 0 or value > 100:
                raise forms.ValidationError(
                    _('El coeficiente debe ser un valor '
                      'entre 0 y 100')
                )

        return value
