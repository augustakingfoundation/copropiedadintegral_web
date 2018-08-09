import re

from django import forms
from django.forms import modelformset_factory
from django.utils.translation import gettext_lazy as _

from buildings.data import BUILDING_DOCUMENT_TYPE_CC
from buildings.data import BUILDING_DOCUMENT_TYPE_NIT
from buildings.data import MEMBERSHIP_TYPE_ACCOUNTANT
from buildings.data import MEMBERSHIP_TYPE_ACCOUNTING_ASSISTANT
from buildings.data import MEMBERSHIP_TYPE_ADMINISTRATIVE_ASSISTANT
from buildings.data import MEMBERSHIP_TYPE_ADMINISTRATOR
from buildings.data import MEMBERSHIP_TYPE_FISCAL_REVIEWER
from buildings.data import VEHICLE_TYPE_CAR
from buildings.data import VEHICLE_TYPE_MOTORCYCLE
from buildings.models import Building
from buildings.models import BuildingMembership
from buildings.models import DomesticWorker
from buildings.models import EmergencyContact
from buildings.models import Leaseholder
from buildings.models import Owner
from buildings.models import ParkingLot
from buildings.models import Pet
from buildings.models import Resident
from buildings.models import Unit
from buildings.models import UnitDataUpdate
from buildings.models import Vehicle
from buildings.models import Visitor


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
    Unit owner form. It's used to define the
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
            'is_resident',
            'is_main',
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
    Unit leaseholder form. It's used to define the
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
            'is_main',
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
    Parking lot form. The unit field included in the
    model is excluded from the form and this value is
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


class VehicleForm(forms.ModelForm):
    """
    Vehicle form. The unit field included in the
    model is excluded from the form and this value is
    assigned in the vehicle create view, in the
    post request.
    """
    class Meta:
        model = Vehicle
        fields = (
            'brand',
            'vehicle_type',
            'license_plate',
            'color',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        fields = [
            'brand',
            'license_plate',
            'color',
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
        vehicle_type = cleaned_data.get('vehicle_type')

        if (
            vehicle_type in (VEHICLE_TYPE_CAR, VEHICLE_TYPE_MOTORCYCLE) and
            not cleaned_data.get('license_plate')
        ):
            self.add_error(
                'license_plate',
                _('Para carros y motocicletas la placa es requerida.'),
            )


class DomesticWorkerForm(forms.ModelForm):
    """
    Domestic worker form. The unit field included in the
    model is excluded from the form and this value is
    assigned in the domestic worker create view, in the
    post request.
    """
    class Meta:
        model = DomesticWorker
        fields = (
            'first_name',
            'last_name',
            'document_type',
            'document_number',
            'schedule',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        fields = [
            'first_name',
            'last_name',
            'document_number',
            'schedule',
        ]

        # Here we are defining the placeholder for each
        # form field. The field labels are used to set
        # the field placeholder automatically.
        for field in fields:
            label = self.fields[field].label
            self.fields[field].label = ''
            self.fields[field].widget.attrs['placeholder'] = label


class PetForm(forms.ModelForm):
    """
    Pet form. The unit field included in the
    model is excluded from the form and this value is
    assigned in the pet create view, in the
    post request.
    """
    class Meta:
        model = Pet
        fields = (
            'pet_type',
            'breed',
            'name',
            'color',
            'picture',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        fields = [
            'pet_type',
            'breed',
            'name',
            'color',
            'picture',
        ]

        # Here we are defining the placeholder for each
        # form field. The field labels are used to set
        # the field placeholder automatically.
        for field in fields:
            label = self.fields[field].label
            self.fields[field].label = ''
            self.fields[field].widget.attrs['placeholder'] = label


class VisitorForm(forms.ModelForm):
    """
    Authorized visitor form. The unit field included in the
    model is excluded from the form and this value is
    assigned in the visitor create view, in the
    post request.
    """
    class Meta:
        model = Visitor
        fields = (
            'first_name',
            'last_name',
            'document_type',
            'document_number',
            'relationship',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        fields = [
            'first_name',
            'last_name',
            'document_number',
            'relationship',
        ]

        # Here we are defining the placeholder for each
        # form field. The field labels are used to set
        # the field placeholder automatically.
        for field in fields:
            label = self.fields[field].label
            self.fields[field].label = ''
            self.fields[field].widget.attrs['placeholder'] = label


class ResidentForm(forms.ModelForm):
    """
    Residents form. The unit field included in the
    model is excluded from the form and this value is
    assigned in the resident create view, in the
    post request.
    """
    class Meta:
        model = Resident
        fields = (
            'first_name',
            'last_name',
            'birthdate',
            'document_type',
            'document_number',
            'mobile_phone',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        fields = [
            'first_name',
            'last_name',
            'birthdate',
            'document_type',
            'document_number',
            'mobile_phone',
        ]

        # Here we are defining the placeholder for each
        # form field. The field labels are used to set
        # the field placeholder automatically.
        for field in fields:
            label = self.fields[field].label
            self.fields[field].label = ''
            self.fields[field].widget.attrs['placeholder'] = label


class EmergencyContactForm(forms.ModelForm):
    """
    Emergency contact form. The unit field included in the
    model is excluded from the form and this value is
    assigned in the resident create view, in the
    post request.
    """
    class Meta:
        model = Resident
        fields = (
            'first_name',
            'last_name',
            'mobile_phone',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        fields = [
            'first_name',
            'last_name',
            'mobile_phone',
        ]

        # Here we are defining the placeholder for each
        # form field. The field labels are used to set
        # the field placeholder automatically.
        for field in fields:
            label = self.fields[field].label
            self.fields[field].label = ''
            self.fields[field].widget.attrs['placeholder'] = label


EmergencyContactFormSet = modelformset_factory(
    EmergencyContact,
    form=EmergencyContactForm,
    extra=0,
    max_num=3,
    min_num=0,
    validate_min=False,
    can_delete=True,
)


class UserSearchForm(forms.Form):
    """User search form. This form is used to
    search a registered user by the email attribute.
    """
    email = forms.EmailField(
        required=True,
        label=_('correo electrónico'),
        widget=forms.EmailInput(
            attrs={
                'placeholder': _('Correo electrónico'),
            },
        ),
        help_text=_(
            'Ingrese la dirección de correo electrónico'
            ' de un usuario registrado en la aplicación'
            ' para crear una membresía en esta copropiedad.'
            ' Si el correo electrónico no se encuentra registrado,'
            ' tendrá la posibilidad de enviarle una invitación para'
            ' que cree una cuenta en la plataforma.'
        )
    )


class MembershipForm(forms.ModelForm):
    """
    Building memberships form. The building field includedin
    the model is excluded from the form and this value is
    assigned in the membership create view, in the
    post request.
    """
    class Meta:
        model = BuildingMembership
        fields = (
            'user',
            'membership_type',
        )

    def __init__(self, *args, **kwargs):
        self.building = kwargs.pop('building')
        self.update = kwargs.pop('update')
        self.membership = kwargs.pop('membership')

        super().__init__(*args, **kwargs)

        if self.membership.is_administrator:
            choices = (
                ('', _('Tipo de membresía')),
                (
                    MEMBERSHIP_TYPE_ADMINISTRATIVE_ASSISTANT,
                    _('Asistente administrativo')
                ),
                (MEMBERSHIP_TYPE_ACCOUNTANT, _('Contador')),
                (
                    MEMBERSHIP_TYPE_ACCOUNTING_ASSISTANT,
                    _('Asistente contable')
                ),
                (MEMBERSHIP_TYPE_FISCAL_REVIEWER, _('Revisor fiscal')),
            )
            # Remove administrator from membership type field
            # if the user is common administrator.
            self.fields['membership_type'].choices = choices

    def clean_user(self):
        # Validations for the user field. A user
        # only can have a membership role per
        # condo.
        value = self.cleaned_data['user']

        if not self.update:
            if BuildingMembership.objects.filter(
                building=self.building,
                user=value,
            ):
                raise forms.ValidationError(
                    _('Ya existe una membresía para este '
                      'usuario en la copropiedad.')
                )

        return value

    def clean_membership_type(self):
        # Validations for the membership type field.
        value = self.cleaned_data['membership_type']

        # Each condo can have a maximun of two users with
        # administrator memberships.
        if (
            BuildingMembership.objects.filter(
                building=self.building,
                membership_type=MEMBERSHIP_TYPE_ADMINISTRATOR,
            ).count() >= 3 and
            value == MEMBERSHIP_TYPE_ADMINISTRATOR
        ):
            raise forms.ValidationError(
                _('El máximo número de membresías de administradores '
                  'por copropiedad es de 3.')
            )

        # Each condo can have only one user with accountant membership.
        if (
            BuildingMembership.objects.filter(
                building=self.building,
                membership_type=MEMBERSHIP_TYPE_ACCOUNTANT,
            ) and
            value == MEMBERSHIP_TYPE_ACCOUNTANT
        ):
            raise forms.ValidationError(
                _('Solo puede existir una membresía de contador activa.')
            )

        # Each condo can have only one user
        # with accounting assistant membership.
        if (
            BuildingMembership.objects.filter(
                building=self.building,
                membership_type=MEMBERSHIP_TYPE_ACCOUNTING_ASSISTANT,
            ) and
            value == MEMBERSHIP_TYPE_ACCOUNTING_ASSISTANT
        ):
            raise forms.ValidationError(
                _('Solo puede existir una membresía'
                  ' de asistente contable activa.')
            )

        # Each condo can have only one user with fiscal reviewer membership.
        if (
            BuildingMembership.objects.filter(
                building=self.building,
                membership_type=MEMBERSHIP_TYPE_FISCAL_REVIEWER,
            ) and
            value == MEMBERSHIP_TYPE_FISCAL_REVIEWER
        ):
            raise forms.ValidationError(
                _('Solo puede existir una membresía de revisor fiscal '
                  'activa.')
            )

        return value


class ConfirmOwnerUpdateForm(forms.ModelForm):
    """Form used to confirm if unit owners must be
    considered for data update.
    """
    update = forms.BooleanField(
        required=False,
        initial=True,
    )

    class Meta:
        model = Owner
        fields = (
            'unit',
            'update',
        )


ConfirmOwnerUpdateFormSet = modelformset_factory(
    UnitDataUpdate,
    form=ConfirmOwnerUpdateForm,
    extra=0,
    min_num=0,
    validate_min=False,
    can_delete=False,
)


class ConfirmLeaseholderUpdateForm(forms.ModelForm):
    """Form used to confirm if unit leaseholders must be
    considered for data update.
    """
    update = forms.BooleanField(
        required=False,
        initial=True,
    )

    class Meta:
        model = Leaseholder
        fields = (
            'unit',
            'update',
        )


ConfirmLeaseholderUpdateFormSet = modelformset_factory(
    UnitDataUpdate,
    form=ConfirmLeaseholderUpdateForm,
    extra=0,
    min_num=0,
    validate_min=False,
    can_delete=False,
)


class ConfirmResidentUpdateForm(forms.ModelForm):
    """Form used to confirm if unit residents must be
    considered for data update.
    """
    update = forms.BooleanField(
        required=False,
        initial=True,
    )

    class Meta:
        model = UnitDataUpdate
        fields = (
            'unit',
            'update',
        )


ConfirmResidentUpdateFormSet = modelformset_factory(
    UnitDataUpdate,
    form=ConfirmResidentUpdateForm,
    extra=0,
    min_num=0,
    validate_min=False,
    can_delete=False,
)


class OwnerUpdateForm(forms.ModelForm):
    """
    Unit owner update form. It's used to define the
    OwnerUpdateFormSet structure, available for update
    owners data directly from a non-authenticated user.
    """
    class Meta:
        model = Owner
        fields = (
            'mobile_phone',
            'phone_number',
            'correspondence_address',
            'email',
        )


OwnerUpdateFormSet = modelformset_factory(
    Owner,
    form=OwnerUpdateForm,
    extra=0,
    min_num=0,
    validate_min=False,
    can_delete=False,
)


class LeaseholderUpdateForm(forms.ModelForm):
    """
    Unit leaseholder update form. It's used to define the
    LeaseholderUpdateFormSet structure, available for update
    leaseholders data directly from a non-authenticated user.
    """
    class Meta:
        model = Leaseholder
        fields = (
            'mobile_phone',
            'phone_number',
            'email',
        )


LeaseholderUpdateFormSet = modelformset_factory(
    Leaseholder,
    form=LeaseholderUpdateForm,
    extra=0,
    min_num=0,
    validate_min=False,
    can_delete=False,
)


ResidentUpdateFormSet = modelformset_factory(
    Resident,
    form=ResidentForm,
    extra=0,
    min_num=0,
    validate_min=False,
    can_delete=False,
)

VisitorUpdateFormSet = modelformset_factory(
    Visitor,
    form=VisitorForm,
    extra=0,
    min_num=0,
    validate_min=False,
    can_delete=False,
)


class membershipTransferForm(forms.Form):
    """
    Transfer membership form. Only main administrators can
    transfer their own membership and only can transfer
    memberships to users with active administrator membership
    in the condo.
    """
    user_to = forms.ModelChoiceField(
        queryset=BuildingMembership.objects.none()
    )

    def __init__(self, *args, **kwargs):
        self.administrators_queryset = kwargs.pop('administrators_queryset')
        super().__init__(*args, **kwargs)

        self.fields['user_to'].queryset = self.administrators_queryset
