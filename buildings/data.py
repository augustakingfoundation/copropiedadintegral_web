from django.utils.translation import ugettext as _


BUILDING_DOCUMENT_TYPE_CC = 1
BUILDING_DOCUMENT_TYPE_NIT = 2
BUILDING_DOCUMENT_TYPE_OTHER = 3

BUILDING_DOCUMENT_TYPE_CHOICES = (
    ('', _('Tipo de documento')),
    (BUILDING_DOCUMENT_TYPE_CC, 'C.C.'),
    (BUILDING_DOCUMENT_TYPE_NIT, 'NIT'),
    (BUILDING_DOCUMENT_TYPE_OTHER, _('Otro')),
)

PARKING_LOT_ASSIGNED = 1
PARKING_LOT_OWN = 2

PARKING_LOT_TYPE_CHOICES = (
    ('', _('Tipo de parqueadero')),
    (PARKING_LOT_ASSIGNED, _('Asignado (Arrendado o Temporal por sorteo)')),
    (PARKING_LOT_OWN, _('Propio')),
)


VEHICLE_TYPE_CAR = 1
VEHICLE_TYPE_MOTORCYCLE = 2
VEHICLE_TYPE_BICYCLE = 3

VEHICLE_TYPE_CHOICES = (
    ('', _('Tipo de vehículo')),
    (VEHICLE_TYPE_CAR, _('Carro')),
    (VEHICLE_TYPE_MOTORCYCLE, _('Motocicleta')),
    (VEHICLE_TYPE_BICYCLE, _('Bicicleta')),
)


MEMBERSHIP_TYPE_ADMINISTRATOR = 1
MEMBERSHIP_TYPE_ADMINISTRATIVE_ASSISTANT = 2
MEMBERSHIP_TYPE_ACCOUNTANT = 3
MEMBERSHIP_TYPE_ACCOUNTING_ASSISTANT = 4
MEMBERSHIP_TYPE_FISCAL_REVIEWER = 5

# MEMBERSHIP_TYPE_ACCOUNTING_ASSISTANT is not included into the
# choices because it is added only for users with
# accuntant membershipsin a deferent way.
MEMBERSHIP_TYPE_CHOICES = (
    ('', _('Tipo de membresía')),
    (MEMBERSHIP_TYPE_ADMINISTRATOR, _('Administrador')),
    (MEMBERSHIP_TYPE_ADMINISTRATIVE_ASSISTANT, _('Asistente administrativo')),
    (MEMBERSHIP_TYPE_ACCOUNTANT, _('Contador')),
    (MEMBERSHIP_TYPE_FISCAL_REVIEWER, _('Revisor fiscal')),
)
