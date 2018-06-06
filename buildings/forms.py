import re

from django import forms

from .data import BUILDING_DOCUMENT_TYPE_NIT
from .data import BUILDING_DOCUMENT_TYPE_CC
from .models import Building
from .models import Unit


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
        self.fields['city'].empty_label = 'Ciudad'

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
                'El NIT ingresado no es válido. Ej: 12345678-1',
            )

        elif (
            document_type == BUILDING_DOCUMENT_TYPE_CC and
            not re.match(r'^\d{5,15}$', document_number)
        ):
            self.add_error(
                'document_number',
                'El documento ingresado solo debe contener números',
            )


class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = (
            'block',
            'unit',
            'area',
            'real_estate_registration',
            'owner_name',
            'owner_document_type',
            'owner_document_number',
            'owner_mobile_phone',
            'owner_phone_number',
            'owner_email',
            'correspondence_address',
            'leaseholder_name',
            'leaseholder_mobile_phone',
            'leaseholder_phone_number',
            'leaseholder_email',
            'observations',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        fields = [
            'block',
            'unit',
            'area',
            'real_estate_registration',
            'owner_name',
            'owner_document_type',
            'owner_document_number',
            'owner_mobile_phone',
            'owner_phone_number',
            'owner_email',
            'correspondence_address',
            'leaseholder_name',
            'leaseholder_mobile_phone',
            'leaseholder_phone_number',
            'leaseholder_email',
            'observations',
        ]

        for field in fields:
            label = self.fields[field].label
            self.fields[field].label = ''
            self.fields[field].widget.attrs['placeholder'] = label
