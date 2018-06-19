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
