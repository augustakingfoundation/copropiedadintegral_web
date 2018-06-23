import re

from django import forms
from django.forms import modelformset_factory
from django.utils.translation import gettext_lazy as _

from .data import BUILDING_DOCUMENT_TYPE_CC
from .data import BUILDING_DOCUMENT_TYPE_NIT
from .models import Building
from .models import Leaseholder
from .models import Owner
from .models import ParkingLot
from .models import Unit


class BuildingForm(forms.ModelForm):
    """
    Building or condo form.
    """
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

        # Here we are defining the placeholder for each
        # form field. The field labels are used to set
        # the field placeholder automatically.
        for field in fields:
            label = self.fields[field].label
            self.fields[field].label = ''
            self.fields[field].widget.attrs['placeholder'] = label

    def clean(self):
        cleaned_data = super().clean()
        document_type = cleaned_data.get('document_type')
        document_number = cleaned_data.get('document_number')

        # Validating document type NIT to fits the Colombian
        # standar. Example Ej: 12345678-1
        if (
            document_type == BUILDING_DOCUMENT_TYPE_NIT and
            not re.match(r'^\d{5,15}-\d{1}$', document_number)
        ):
            self.add_error(
                'document_number',
                _('El NIT ingresado no es válido. Ej: 12345678-1'),
            )

        # Validating document type CC to fits the Colombian
        # standar. This value must contain only numbers.
        elif (
            document_type == BUILDING_DOCUMENT_TYPE_CC and
            not re.match(r'^\d{5,15}$', document_number)
        ):
            self.add_error(
                'document_number',
                _('El documento ingresado solo debe contener números'),
            )


class OwnerForm(forms.ModelForm):
    """
    Unit owner form. It's user to define the
    OwnerFormSet structure.
    """
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

        # Here we are defining the placeholder for each
        # form field. The field labels are used to set
        # the field placeholder automatically.
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
    """
    Unit leaseholder form. It's user to define the
    Leaseholder FormSet structure.
    """
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

        # Here we are defining the placeholder for each
        # form field. The field labels are used to set
        # the field placeholder automatically.
        for field in fields:
            label = self.fields[field].label
            self.fields[field].label = ''
            self.fields[field].widget.attrs['placeholder'] = label


LeaseholderFormSet = modelformset_factory(
    Leaseholder,
    form=LeaseholderForm,
    extra=0,
    max_num=2,
    min_num=0,
    validate_min=False,
    can_delete=True,
)


class UnitForm(forms.ModelForm):
    """
    Unit form (Apartment, house or office).
    """
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

        # Here we are defining the placeholder for each
        # form field. The field labels are used to set
        # the field placeholder automatically.
        for field in fields:
            label = self.fields[field].label
            self.fields[field].label = ''
            self.fields[field].widget.attrs['placeholder'] = label

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


class ParkingLotForm(forms.ModelForm):
    """
    Parking log form. The unit field included in the
    model is excluded from the from and this value is
    assigned in the parking lot create view, in the
    post request.
    """
    class Meta:
        model = ParkingLot
        fields = (
            'number',
            'parking_lot_type',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['number'].widget.attrs['placeholder'] = _('Número/ID')
